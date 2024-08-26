# Crafting Interpreters: plox

An implementation of Robert Nystrom's Lox programming language in Python. Based on the jlox implementation from his book Crafting Interpreters.

## Implementation Notes

### Internal Representation of Values

| Lox     | Python |
|---------|--------|
| number  | float  |
| string  | str    |
| boolean | bool   |
| nil     | None   |
