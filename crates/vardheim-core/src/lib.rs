#![no_std]
#![forbid(unsafe_code)]
#![doc = "Runtime-independent ACME protocol foundations for Vardheim."]

/// Identifies this crate's architectural responsibility.
pub const CRATE_ROLE: &str = "protocol";

#[cfg(test)]
mod tests {
    use super::CRATE_ROLE;

    #[test]
    fn role_is_stable() {
        assert_eq!(CRATE_ROLE, "protocol");
    }
}
