use pyo3::prelude::*;
use ipnetwork::{Ipv4Network, Ipv6Network};
use std::net::{Ipv4Addr, Ipv6Addr};
use std::str::FromStr;

#[pyfunction]
fn is_ipv4_in_cidr(ip: &str, cidr: &str) -> PyResult<bool> {
    let ip_addr = ip.parse::<Ipv4Addr>()
        .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid IPv4 address"))?;

    let cidr_net = Ipv4Network::from_str(cidr)
        .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid IPv4 CIDR notation"))?;

    Ok(cidr_net.contains(ip_addr))
}

#[pyfunction]
fn is_ipv6_in_cidr(ip: &str, cidr: &str) -> PyResult<bool> {
    let ip_addr = ip.parse::<Ipv6Addr>()
        .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid IPv6 address"))?;

    let cidr_net = Ipv6Network::from_str(cidr)
        .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid IPv6 CIDR notation"))?;

    Ok(cidr_net.contains(ip_addr))
}

#[pymodule]
fn rs_cidr_verifier(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(is_ipv4_in_cidr, m)?)?;
    m.add_function(wrap_pyfunction!(is_ipv6_in_cidr, m)?)?;

    Ok(())
}
