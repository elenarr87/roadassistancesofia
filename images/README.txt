Placeholder guidance for images used in index.html.

To fully benefit from srcset/AVIF optimizations, provide the following files in the `images/` directory:
- dark.avif, dark@2x.avif, dark.webp, dark@2x.webp
- ive.avif, ive@2x.avif, ive.webp, ive@2x.webp
- old.avif, old@2x.avif, old.webp, old@2x.webp
- red.avif, red@2x.avif, red.webp, red@2x.webp
- mot.avif, mot@2x.avif, mot.webp, mot@2x.webp
- pik.avif, pik@2x.avif, pik.webp, pik@2x.webp

If you cannot provide AVIF versions, at minimum include the WebP files referenced.

Tools to generate optimized formats:
- sharp (node): https://github.com/lovell/sharp
- cwebp / avifenc

Example sharp command (node script):

const sharp = require('sharp');
sharp('images/dark.webp').avif({quality:60}).toFile('images/dark.avif');

