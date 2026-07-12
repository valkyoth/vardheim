#![no_std]
#![forbid(unsafe_code)]
#![doc = "Runtime-independent TLS ACME challenge primitives for Vardheim."]

/// The TLS-ALPN-01 validation method registered by ACME.
pub const TLS_ALPN_01: &str = "tls-alpn-01";

#[cfg(test)]
mod tests {
    use super::TLS_ALPN_01;

    #[test]
    fn tls_alpn_01_name_matches_the_registry() {
        assert_eq!(TLS_ALPN_01, "tls-alpn-01");
    }
}
