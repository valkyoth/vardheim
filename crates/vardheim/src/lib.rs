#![no_std]
#![forbid(unsafe_code)]
#![doc = "The public Vardheim facade."]

/// Low-level, runtime-independent ACME protocol foundations.
pub use vardheim_core as core;
/// ACME challenge families.
pub mod challenge {
    /// DNS challenge primitives and provider boundaries.
    pub use vardheim_challenge_dns as dns;
    /// HTTP challenge primitives and presentation boundaries.
    pub use vardheim_challenge_http as http;
    /// TLS challenge identity primitives.
    pub use vardheim_challenge_tls as tls;
}

/// The current workspace foundation version.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

#[cfg(test)]
mod tests {
    use super::{VERSION, challenge, core};

    #[test]
    fn facade_exposes_every_foundation_boundary() {
        assert_eq!(VERSION, "0.1.0");
        assert_eq!(core::CRATE_ROLE, "protocol");
        assert_eq!(challenge::http::HTTP_01, "http-01");
        assert_eq!(challenge::dns::DNS_01, "dns-01");
        assert_eq!(challenge::tls::TLS_ALPN_01, "tls-alpn-01");
    }
}
