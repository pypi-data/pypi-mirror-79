#include <Eigen/Core>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <cmath>
#include <vector>
#include <boost/math/special_functions/gamma.hpp>


namespace py = pybind11;

int eulerian(int n, int m){
    if (m >= n or n == 0){
        return 0;
    }
    if (m == 0){
        return 1;
    }
    return ((n - m) * eulerian(n - 1, m - 1) + (m + 1) * eulerian(n - 1, m));
}

std::vector<double> eulerian_all(int n){
    int i = 0;
    std::vector<double> res(n);
    for(i = 0; i < n; i++){
        res[i] = eulerian(n, i);
    }
    return res;
}

double log1mexp(double x){
    if(x <= std::log(2.0)){
        return std::log(-std::expm1(-x));
    }else{
        return std::log1p(-std::exp(-x));
    }
}


std::vector<double> log1mexpvec(std::vector<double> x){
    std::vector<double>::size_type i = 0;;
    double eps = std::log(2.0);
    std::vector<double> res(x.size());
    for(i = 0; i < x.size(); i++){
        if(x[i] <= eps){
            res[i] = std::log(-std::expm1(-x[i]));
        }else{
            res[i] = std::log1p(-std::exp(-x[i]));
        }
    }
    return res;
}


double polyneval(
    std::vector<double> p,
    double x
){
    std::vector<double>::size_type i = 0;
    double res = 0.0;
    for(i=0; i<p.size(); i++){
        res = res * x + p[i];
    }
    return res;
}


std::vector<double> polyneval(
    std::vector<double> p,
    std::vector<double> x,
    bool is_log_z = false
){
    std::vector<double>::size_type i = 0;
    std::vector<double> res(x.size());
    if(is_log_z){
        for(i=0; i<x.size(); i++){
            res[i] = polyneval(p, std::exp(x[i]));
        }
    }else{
        for(i=0; i<x.size(); i++){
            res[i] = polyneval(p, x[i]);
        }
    }
    return res;
}

Eigen::VectorXd polyneval(
    std::vector<double> p,
    Eigen::VectorXd x,
    bool is_log_z = false
){
    Eigen::EigenBase<Eigen::VectorXd>::Index i = 0;
    Eigen::VectorXd res = Eigen::VectorXd(x.size());
    if(is_log_z){
        for(i=0; i<x.size(); i++){
            res(i) = polyneval(p, std::exp(x(i)));
        }
    }else{
        for(i=0; i<x.size(); i++){
            res(i) = polyneval(p, x(i));
        }
    }
    return res;
}


py::array_t<double> polyneval_py(
    py::array_t<double> coef,
    py::array_t<double> x,
    bool is_log_z = false
){
    return py::cast(
        polyneval(
            coef.cast<std::vector<double>>(),
            x.cast<Eigen::VectorXd>(),
            is_log_z
        )
    );
}


std::vector<double> minus_vec(std::vector<double> x){
    std::vector<double>::size_type i = 0;
    std::vector<double> res(x.size());
    for(i=0; i < x.size(); i++){
        res[i] = -x[i];
    }
    return res;
}


std::vector<double> polylog(
    std::vector<double> z,
    int s,
    bool is_log_z=false
){
    std::vector<double>::size_type i = 0;
    std::vector<double> res = polyneval(
        eulerian_all(-s),
        z,
        is_log_z
    );
    if(is_log_z){
        for(i=0; i<z.size(); i++){
            res[i] = std::log(res[i]) + \
            z[i] - (-s + 1.0) * log1mexp(-z[i]);
        }
    }else{
        for(i=0; i<z.size(); i++){
            res[i] = std::log(res[i]) + \
            std::log(z[i]) - (-s + 1.0) * std::log1p(-z[i]);
        }
    }
    return res;
}


Eigen::VectorXd polylog(
    Eigen::VectorXd z,
    int s,
    bool is_log_z=false
){
    Eigen::EigenBase<Eigen::VectorXd>::Index i = 0;
    Eigen::VectorXd res = polyneval(
        eulerian_all(-s),
        z,
        is_log_z
    );
    if(is_log_z){
        for(i=0; i<z.size(); i++){
            res(i) = std::log(res(i)) + \
            z(i) - (-s + 1.0) * log1mexp(-z(i));
        }
    }else{
        for(i=0; i<z.size(); i++){
            res(i) = std::log(res(i)) + \
            std::log(z(i)) - (-s + 1.0) * std::log1p(-z(i));
        }
    }
    return res;
}


py::array_t<double> polylog_py(
    py::array_t<double> z,
    int s,
    bool is_log_z=false
){
    return py::cast(
        polylog(
            z.cast<Eigen::VectorXd>(),
            s,
            is_log_z
        )
    );
}


Eigen::VectorXd pdf_frank(
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> u_values,
    double theta,
    bool is_log = false){
    Eigen::VectorXd dcopula;
    if(theta == 0.0){
        dcopula.setZero(
            u_values.rows()
        );
        return dcopula;
    }
    int d;
    double lp;
    Eigen::VectorXd usum = Eigen::VectorXd(u_values.rows());
    Eigen::VectorXd lu = Eigen::VectorXd(u_values.rows());
    Eigen::VectorXd li = Eigen::VectorXd(u_values.rows());
    Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic> lpu = \
        Eigen::MatrixXd(u_values.rows(), u_values.cols());
    Eigen::VectorXd lpusum = Eigen::VectorXd(u_values.rows());
    d = u_values.cols();
    usum = u_values.rowwise().sum();
    lp = log1mexp(theta);
    lpu = (u_values.array() * theta).unaryExpr(&log1mexp).matrix();
    lu = lpu.rowwise().sum();
    lpu = (lpu.array() - lp).matrix();
    lpusum = lpu.rowwise().sum();
    lpusum = (lp + lpusum.array()).matrix();
    li = polylog(
        lpusum,
        -(d - 1),
        true
    );
    dcopula = (d - 1.0) * std::log(theta) + \
    (li - (usum.array() * theta).matrix() - lu).array();
    if(is_log){
        return dcopula;
    }
    return dcopula.array().exp();
}

py::array_t<double> pdf_frank_py(
    py::array_t<double> u_values,
    double theta,
    bool is_log = false
){
    return py::cast(
        pdf_frank(
            u_values.cast<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic>>(),
            theta,
            is_log
        )
    );
}


Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> ipsi_clayton(
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> u_values,
    double theta,
    bool is_log = false){
    Eigen::Matrix<double,
        Eigen::Dynamic,
        Eigen::Dynamic> res;
    res.setZero(
            u_values.rows(),
            u_values.cols()
        );
    double theta_sign = 1.0;
    if(theta < 0.0){
        theta_sign = -1.0;
    }
    res = theta_sign * ((u_values.array().pow(-theta)) - 1.0);
    if(is_log){
        return res.array().log();
    }
    return res;
}


py::array_t<double> ipsi_clayton_py(
    py::array_t<double> u_values,
    double theta,
    bool is_log = false
){
    return py::cast(
        ipsi_clayton(
            u_values.cast<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic>>(),
            theta,
            is_log
        )
    );
}


Eigen::VectorXd pdf_clayton(
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> u_values,
    double theta,
    bool is_log = false){
    if (theta == 0.0){
        return Eigen::VectorXd::Zero(u_values.rows());
    }
    Eigen::VectorXd res(u_values.rows());
    double d = float(u_values.cols());
    Eigen::VectorXd lu = u_values.array().log().matrix().rowwise().sum();
    Eigen::VectorXd t_var = ipsi_clayton(u_values, theta, false).rowwise().sum();
    if(theta < 0.0){
        for(auto i = 0; i < u_values.rows(); i++){
            if(t_var(i) < 1.0){
                res(i) = std::log1p(theta);
                res(i) -= (1.0 + theta) * lu(i);
                res(i) -= (d + 1.0 / theta) * std::log1p(-t_var(i));
            }else{
                res(i) = NAN;
            }
        }
    }else{
        res = (
            theta * (
                Eigen::VectorXd::LinSpaced(int(d) - 1, 1.0, d - 1.0)
            ).array()
        ).log1p();
        res = res.matrix().sum() - (1.0 + theta) * lu.array() - (
            d + 1.0 / theta
        ) * t_var.array().log1p();
    }
    if(is_log){
        return res;
    }
    return res.array().exp();
}


py::array_t<double> pdf_clayton_py(
    py::array_t<double> u_values,
    double theta,
    bool is_log = false
){
    return py::cast(
        pdf_clayton(
            u_values.cast<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic>>(),
            theta,
            is_log
        )
    );
}


Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> ipsi_gumbel(
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> u_values,
    double theta,
    bool is_log = false){
    if(is_log){
        return theta * (-u_values.array().log()).log();
    }
    return (-u_values.array().log()).pow(theta);
}


py::array_t<double> ipsi_gumbel_py(
    py::array_t<double> u_values,
    double theta,
    bool is_log = false
){
    return py::cast(
        ipsi_gumbel(
            u_values.cast<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic>>(),
            theta,
            is_log
        )
    );
}


double fact(double n) {
   if ((n==0.0)||(n==1.0))
   return 1.0;
   else
   return n*fact(n-1.0);
}


int fact(int n) {
   if ((n==0)||(n==1))
   return 1;
   else
   return n*fact(n-1);
}


double log_poisscdf(double k, double lambda){
    return std::log(boost::math::gamma_q(k + 1.0, lambda));
}


Eigen::MatrixXd lpoiss_check(
    Eigen::VectorXd lx_var,
    double alpha_var,
    int d_var){
    Eigen::VectorXd k = Eigen::VectorXd::LinSpaced(d_var, 1.0, double(d_var));
    Eigen::VectorXd x = lx_var.array().exp();
    Eigen::MatrixXd lppois = Eigen::MatrixXd::Zero(d_var, lx_var.size());
    for(auto row = 0; row < d_var; row++){
        for(auto col = 0; col < lx_var.size(); col++){
            lppois(row, col) = log_poisscdf(double(d_var) - k(row), x(col));
        }
    }
    return lppois;
}


py::array_t<double> lpoiss_check_py(
    py::array_t<double> lx_var,
    double alpha_var,
    int d_var
){
    return py::cast(
        lpoiss_check(
            lx_var.cast<Eigen::Matrix<double, 1, Eigen::Dynamic>>(),
            alpha_var,
            d_var
        )
    );
}


Eigen::VectorXd lsum_row(
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> x_values,
    bool is_log = true){
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> b_i;
    if(is_log){
        b_i = x_values;
    }else{
        b_i = x_values.array().log().matrix();
    }
    Eigen::VectorXd b_max = b_i.colwise().maxCoeff();
    Eigen::VectorXd res = Eigen::VectorXd::Zero(b_i.cols());
    for(auto row = 0; row < x_values.rows(); row++){
        for(auto col = 0; col < x_values.cols(); col++){
            b_i(row, col) = std::exp(b_i(row, col) - b_max(col));
            res(col) += b_i(row, col);
        }
    }
    res = res.array().log();
    return b_max + res;
}


Eigen::VectorXd lsum_col(
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> x_values,
    bool is_log = true){
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> b_i;
    if(is_log){
        b_i = x_values;
    }else{
        b_i = x_values.array().log().matrix();
    }
    Eigen::VectorXd b_max = b_i.rowwise().maxCoeff();
    Eigen::VectorXd res = Eigen::VectorXd::Zero(b_i.rows());
    for(auto col = 0; col < x_values.cols(); col++){
        for(auto row = 0; row < x_values.rows(); row++){
            b_i(row, col) = std::exp(b_i(row, col) - b_max(row));
            res(row) += b_i(row, col);
        }
    }
    res = res.array().log();
    return b_max + res;
}


py::array_t<double> lsum_row_py(
    py::array_t<double> x_values,
    bool is_log = true
){
    return py::cast(
        lsum_row(
            x_values.cast<Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic>>(),
            is_log
        )
    );
}
py::array_t<double> lsum_col_py(
    py::array_t<double> x_values,
    bool is_log = true
){
    return py::cast(
        lsum_col(
            x_values.cast<Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic>>(),
            is_log
        )
    );
}


py::array_t<double> lsum_py(
    py::array_t<double> x_values,
    bool is_log = true,
    int axis = 0
){
    if(axis == 0){
        return py::cast(
            lsum_row(
                x_values.cast<Eigen::Matrix<
            double,
            Eigen::Dynamic,
            Eigen::Dynamic>>(),
                is_log
            )
        );
    }else{
        return py::cast(
            lsum_col(
                x_values.cast<Eigen::Matrix<
            double,
            Eigen::Dynamic,
            Eigen::Dynamic>>(),
                is_log
            )
        );
    }
}


Eigen::VectorXd lssum(
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> x_values,
    Eigen::VectorXd x_sign,
    bool is_log = true){
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> b_i;
    if(is_log){
        b_i = x_values;
    }else{
        b_i = x_values.array().log().matrix();
    }
    Eigen::VectorXd b_max = b_i.colwise().maxCoeff();
    for(auto row = 0; row < b_i.rows(); row++){
        for(auto col = 0; col < b_i.cols(); col++){
            b_i(row, col) = x_sign(row) * std::exp(b_i(row, col) - b_max(col));
        }
    }
    Eigen::VectorXd res = b_i.colwise().sum();
    res = res.array().log();
    return b_max + res;
}


py::array_t<double> lssum_py(
    py::array_t<double> x_values,
    py::array_t<double> x_sign,
    bool is_log = true
){
    return py::cast(
        lssum(
            x_values.cast<Eigen::Matrix<
                double,
                Eigen::Dynamic,
                Eigen::Dynamic>>(),
            x_sign.cast<Eigen::Matrix<
                double,
                1,
                Eigen::Dynamic>>(),
            is_log
        )
    );
}


Eigen::VectorXd signff(
    double alpha,
    Eigen::VectorXd j,
    int d){
    Eigen::VectorXd res(j.size());
    if(alpha == 1.0){
        for(auto row = 0; row < j.size(); row++){
            if(j(row) == d){
                res(row) = 1.0;
            }else{
                res(row) = std::pow(-1.0, double(d) - j(row));
            }
        }
    }else{
        double x = 0.0;
        for(auto row = 0; row < j.size(); row++){
            if(j(row) > d){
                res(row) = NAN;
            }else{
                x = alpha * j(row);
                if(x != std::floor(x)){
                    res(row) = std::pow(-1.0, j(row) - std::ceil(x));
                }
            }
        }
    }
    return res;
}


py::array_t<double> signff_py(
    double alpha,
    py::array_t<int> j,
    int d
){
    return py::cast(
        signff(
            alpha,
            j.cast<Eigen::Matrix<
                double,
                1,
                Eigen::Dynamic>>(),
            d
        )
    );
}


Eigen::VectorXd log_polyg(
    Eigen::VectorXd lx_var,
    double alpha_var,
    int d_var){
    Eigen::VectorXd k = Eigen::VectorXd::LinSpaced(d_var, 1.0, double(d_var));
    Eigen::VectorXd x = lx_var.array().exp();
    Eigen::MatrixXd lppois = Eigen::MatrixXd::Zero(d_var, lx_var.size());
    for(auto row = 0; row < d_var; row++){
        for(auto col = 0; col < lx_var.size(); col++){
            lppois(row, col) = log_poisscdf(double(d_var) - k(row), x(col));
        }
    }
    Eigen::MatrixXd llx = k * lx_var.transpose();
    Eigen::VectorXd labspoch = Eigen::VectorXd::Zero(d_var);
    for(auto col = 0; col < d_var; col++){
        for(auto row = 0; row < d_var; row++){
            labspoch(col) += std::log(
                std::abs(alpha_var * double(col + 1) - (k(row) - 1.0))
            );
        }
    }
    Eigen::VectorXd lfac = k.unaryExpr<double(*)(double)>(&fact).array().log();
    Eigen::MatrixXd lxabs = Eigen::MatrixXd::Zero(d_var, lx_var.size());
    for(auto row = 0; row < d_var; row++){
        for(auto col = 0; col < lx_var.size(); col++){
            lxabs(row, col) = llx(row, col) + lppois(row, col) + (
                labspoch(row) - lfac(row)
            ) + x(col);
        }
    }
    return lssum(lxabs, signff(alpha_var, k, d_var), true);
}


py::array_t<double> log_polyg_py(
    py::array_t<double> lx_var,
    double alpha_var,
    int d_var
){
    return py::cast(
        log_polyg(
            lx_var.cast<Eigen::Matrix<double, 1, Eigen::Dynamic>>(),
            alpha_var,
            d_var
        )
    );
}


Eigen::VectorXd pdf_gumbel(
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> u_values,
    double theta,
    bool is_log = false){
    Eigen::VectorXd dcopula(u_values.rows());
    double d = double(u_values.cols());
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> mlu = -u_values.array().log();
    Eigen::Matrix<
        double,
        Eigen::Dynamic,
        Eigen::Dynamic> lmlu = mlu.array().log();
    Eigen::MatrixXd lip = ipsi_gumbel(u_values, theta, true);
    Eigen::VectorXd lnt = lsum_col(lip, true);
    double alpha = 1.0 / theta;
    Eigen::VectorXd lx = (alpha * lnt.array()).matrix();
    Eigen::VectorXd ls = log_polyg(
        lx, alpha, int(d)
    ).array() - d * lx.array() / alpha;
    Eigen::VectorXd lnc = -lx.array().exp();
    dcopula = lnc.array() + d * std::log(theta) + (
        (theta - 1.0) * lmlu.array() + mlu.array()
    ).rowwise().sum() + ls.array();
    if(is_log){
        return dcopula;
    }
    return dcopula.array().exp();
}


py::array_t<double> pdf_gumbel_py(
    py::array_t<double> u_values,
    double theta,
    bool is_log = false
){
    return py::cast(
        pdf_gumbel(
            u_values.cast<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic>>(),
            theta,
            is_log
        )
    );
}

PYBIND11_MODULE(c_archimedean, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------
        .. currentmodule:: python_example
        .. autosummary::
           :toctree: _generate
           add
           subtract
    )pbdoc";

    m.def("eulerian", &eulerian, R"pbdoc(
        Return eulerian number A(n, m)
        :param n: int
        :param m: int
        :return:
    )pbdoc",
    py::arg("n"), py::arg("m"));

    m.def("eulerian_all", &eulerian_all, R"pbdoc(
        compute eulerian number
        :param n: int
        :return:
        >>> eulerian_all(10)
        array([1.000000e+00, 1.013000e+03, 4.784000e+04, 4.551920e+05,
               1.310354e+06, 1.310354e+06, 4.551920e+05, 4.784000e+04,
               1.013000e+03, 1.000000e+00])
    )pbdoc",
    py::arg("n"), py::return_value_policy::take_ownership);

    m.def("log1mexp", &log1mexp, R"pbdoc(
        compute log(1-exp(-a))
        :param x: double
        :return:
    )pbdoc",
    py::arg("x"));

    m.def("log1mexpvec", &log1mexpvec, R"pbdoc(
        compute log(1-exp(-a)
        :param x: [double]
        :return:
    )pbdoc",
    py::arg("x"));

    m.def("polyneval", &polyneval_py, R"pbdoc(
        :param coef: [double]
        :param x: [double]
        :return:
        >>> polyneval(eulerian_all(10), np.array([-4, -3]))
        array([1.12058925e+08, 9.69548800e+06])
    )pbdoc",
    py::arg("coef"), py::arg("x"), py::arg("is_log_z"));

    m.def("minus_vec", &minus_vec, R"pbdoc(
        compute -x
        :param x: [double]
        :return:
    )pbdoc",
    py::arg("x"));

    m.def("polylog", &polylog_py, R"pbdoc(
        :param z: [double]
        :param s: double
        :param is_log_z: bool
        :return:
        >>> polylog(np.array([0.01556112, 0.00108968, 0.00889932]), -2)
        array([-4.1004881 , -6.81751129, -4.68610299])
    )pbdoc",
    py::arg("z"), py::arg("s"), py::arg("is_log_z"));

    m.def("pdf_frank", &pdf_frank_py, R"pbdoc(
        :param u_values: np.array
        :param theta: double
        :param is_log: bool
        :return:
    )pbdoc",
    py::arg("u_values"), py::arg("theta"), py::arg("is_log"));

    m.def("ipsi_clayton", &ipsi_clayton_py, R"pbdoc(
        :param u_values: np.array
        :param theta: double
        :param is_log: bool
        :return:
    )pbdoc",
    py::arg("u_values"), py::arg("theta"), py::arg("is_log"));

    m.def("pdf_clayton", &pdf_clayton_py, R"pbdoc(
        :param u_values: np.array
        :param theta: double
        :param is_log: bool
        :return:
    )pbdoc",
    py::arg("u_values"), py::arg("theta"), py::arg("is_log"));

    m.def("ipsi_gumbel", &ipsi_gumbel_py, R"pbdoc(
        :param u_values: np.array
        :param theta: double
        :param is_log: bool
        :return:
    )pbdoc",
    py::arg("u_values"), py::arg("theta"), py::arg("is_log"));

    m.def("lsum_row", &lsum_row_py, R"pbdoc(
        :param x_values: np.array
        :param is_log: bool
        :return:
    )pbdoc",
    py::arg("x_values"), py::arg("is_log"));

    m.def("lsum_col", &lsum_col_py, R"pbdoc(
        :param x_values: np.array
        :param is_log: bool
        :return:
    )pbdoc",
    py::arg("x_values"), py::arg("is_log"));

    m.def("lsum", &lsum_py, R"pbdoc(
        :param x_values: np.array
        :param axis: int
        :param is_log: bool
        :return:
    )pbdoc",
    py::arg("x_values"), py::arg("axis"), py::arg("is_log"));

    m.def("lssum", &lssum_py, R"pbdoc(
        :param x_values: np.array
        :param x_sign: np.array
        :param is_log: bool
        :return:
    )pbdoc",
    py::arg("x_values"), py::arg("x_sign"), py::arg("is_log"));

    m.def("signff", &signff_py, R"pbdoc(
        :param alpha: double
        :param j: np.array
        :param d: int
        :return:
    )pbdoc",
    py::arg("alpha"), py::arg("j"), py::arg("d"));

    m.def("log_polyg", &log_polyg_py, R"pbdoc(
        :param lx_var: np.array
        :param alpha_var: double
        :param d_var: double
        :return:
    )pbdoc",
    py::arg("lx_var"), py::arg("alpha_var"), py::arg("d_var"));

    m.def("lpoiss_check", &lpoiss_check_py, R"pbdoc(
        :param lx_var: np.array
        :param alpha_var: double
        :param d_var: double
        :return:
    )pbdoc",
    py::arg("lx_var"), py::arg("alpha_var"), py::arg("d_var"));

    m.def("pdf_gumbel", &pdf_gumbel, R"pbdoc(
        :param u_values: np.array
        :param theta: double
        :param is_log: bool
        :return:
    )pbdoc",
    py::arg("u_values"), py::arg("theta"), py::arg("is_log"));
}
