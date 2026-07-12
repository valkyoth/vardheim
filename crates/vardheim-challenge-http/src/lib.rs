#![no_std]
#![forbid(unsafe_code)]
#![doc = "Runtime-independent HTTP ACME challenge primitives for Vardheim."]

/// The HTTP-01 validation method registered by ACME.
pub const HTTP_01: &str = "http-01";

#[cfg(test)]
mod tests {
    use super::HTTP_01;

    #[test]
    fn http_01_name_matches_the_registry() {
        assert_eq!(HTTP_01, "http-01");
    }
}
