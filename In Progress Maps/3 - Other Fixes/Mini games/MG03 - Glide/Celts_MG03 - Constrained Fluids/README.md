### Celts
 - Celts features a section with massive waves made of water blocks floating in the air. 
 Unfortunately, loading these chunks in 1.13+ causes all this floating water to update and spill everywhere. 
 To prevent this, an MCEdit filter was used to place blocks on all sides of every piece of water in this map. Structure Voids were used since they are invisible, stop fluids, and (unlike Barriers) completely intangible.
 
Log:
`
PERFORM BLOCKONDITIONAL
---Omitted more than 120000 lines of finding <Block Water (Still, Level \*) (9:\*)> and placing <Block Structure Void (217:0)>---
Total Blocks Found: 63803
Total Blocks Placed: 47917

MANUAL FIXES - prevent water from flowing over replaceable non-air blocks
Placed <Block Structure Void (217:0)> at (228, 67, 340), replacing <Block Grass (31:1)>
Placed <Block Structure Void (217:0)> at (229, 67, 336), replacing <Block Grass (31:1)>`