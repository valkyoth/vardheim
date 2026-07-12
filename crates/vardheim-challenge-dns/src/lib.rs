#![no_std]
#![forbid(unsafe_code)]
#![doc = "Runtime-independent DNS ACME challenge primitives for Vardheim."]

/// The DNS-01 validation method registered by ACME.
pub const DNS_01: &str = "dns-01";

#[cfg(test)]
mod tests {
    use super::DNS_01;

    #[test]
    fn dns_01_name_matches_the_registry() {
        assert_eq!(DNS_01, "dns-01");
    }
}
