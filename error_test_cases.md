# Error Handling Test Cases

## 1. Unmatched Formatting

This is **bold text without closing asterisks

This is *italic text without closing asterisk

## 2. Malformed Links

This is a [broken link](http://example.com

This is another [broken link]

## 3. Incorrect Header Syntax

#This header has no space after the hash

########## This header has too many hashes

## 4. Unbalanced Code Blocks

```python
def unclosed_code_block():
    return "This block is not closed

## 5. Malformed Tables

| Header 1 | Header 2 | Header 3
|-----------|-----------
| Row 1, Col 1 | Row 1, Col 2 | Row 1, Col 3 |
| Row 2, Col 1 | Row 2, Col 2 |

## 6. Nested Lists with Incorrect Indentation

1. First item
2. Second item
  - Nested item with incorrect indentation
3. Third item
 - Another incorrectly nested item

## 7. Unmatched Blockquotes

> This is a blockquote
> With multiple lines
This line should be in the blockquote but isn't

## 8. Image with Missing Alt Text

![]($http://example.com/image.jpg)

## 9. Horizontal Rule Variations

---
--
****************

## 10. Mixed Inline Formatting

This is **bold _and italic* text** with mismatched delimiters

## 11. Empty Formatting

** **
__ __
`` ``

## 12. Excessive Nesting

> This is a blockquote
>> With a nested blockquote
>>> And another level
>>>> And another
>>>>> And one more for good measure

## 13. Code Blocks with Spaces

    This is an indented code block
  But this line isn't indented enough

## 14. HTML-like content

<p>This looks like HTML but isn't in a code block</p>

## 15. Escape Character Misuse

This \*should\* be \*\*bold\*\* but the escapes are wrong