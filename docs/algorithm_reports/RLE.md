# Run-Length Encoding (RLE)

## 1. Overview
**Run-Length Encoding (RLE)** is a simple and fast form of lossless data compression. It replaces consecutive identical data elements ("runs") with a single data value and its count. RLE is particularly effective for data with long sequences of repeating values, such as simple graphic images (icons, line art) or sparse matrices.

## 2. Definitions
- **Run:** A sequence of consecutive identical symbols in a dataset.
- **Run-Length:** The number of symbols in a run.
- **Encoded Pair:** $(L, V)$ where $L$ is the run-length and $V$ is the data value.

## 3. Theory
The basic principle is to identify a run $v, v, \dots, v$ ($n$ times) and store it as $(n, v)$. 

For example, the string `AAAABBBCCDAA` is encoded as:
- `A` repeated 4 times: `(4, A)`
- `B` repeated 3 times: `(3, B)`
- `C` repeated 2 times: `(2, C)`
- `D` repeated 1 time: `(1, D)`
- `A` repeated 2 times: `(2, A)`
Encoded result: `4A3B2C1D2A`.

### Variants
1.  **Bit-level RLE:** Used for binary images where runs of 0s and 1s alternate. Only lengths need to be stored if the starting bit is known.
2.  **Flagged RLE:** Uses a special marker byte to indicate a run. This avoids expanding non-repeating data.
3.  **PackBits:** An RLE variant used by Apple in TIFF/PDF files, where a signed length byte indicates whether the following bytes are a run or unique data.

## 4. Pseudo Code
```python
def rle_encode(data):
    if not data: return []
    encoded = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i-1]:
            count += 1
        else:
            encoded.append((count, data[i-1]))
            count = 1
    encoded.append((count, data[-1]))
    return encoded

def rle_decode(encoded):
    data = []
    for count, value in encoded:
        data.extend([value] * count)
    return data
```

## 5. Parameters Selections
- **Max Run Length:** Limited by the number of bits used for the count (e.g., 255 if using 1 byte). Longer runs must be split.
- **Encoding Threshold:** Sometimes RLE is only applied to runs longer than a certain threshold to avoid "negative compression."

## 6. Complexity
- **Time Complexity:** $O(N)$ for both encoding and decoding, where $N$ is the number of elements in the data.
- **Space Complexity:**
    - **Best Case:** $O(1)$ if the entire data is one long run.
    - **Worst Case:** $O(2N)$ (or $O(N)$) if no elements repeat.

## 7. Usage
- **Image Formats:** Used in BMP, TIFF, PCX, and early versions of JPEG (for DC coefficients).
- **Fax Machines:** Modified Huffman (RLE + Huffman) is used in Group 3/4 fax compression.
- **Video Games:** Storing 2D tilemaps or sprite data.
- **Bioinformatics:** Encoding genomic sequences with long repeating bases.

## 9. References
1.  Salomon, D. (2007). *Data Compression: The Complete Reference*. Springer.
2.  Sayood, K. (2017). *Introduction to Data Compression*. Morgan Kaufmann.
3.  TIFF Revision 6.0 Specification, Adobe Systems Inc.
