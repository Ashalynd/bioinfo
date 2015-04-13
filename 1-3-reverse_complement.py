"""
Find the reverse complement of a DNA string.
     Input: A DNA string Pattern.
     Output: Pattern, the reverse complement of Pattern.
"""

import bio.io_utils
import bio.pattern

(text,) = bio.io_utils.read_input()
reverse = bio.pattern.reverse(text)

bio.io_utils.emit_or_compare(reverse)