### Conversion Details
- Maps converted to Java Edition using [MCC Tool Chest](https://mcctoolchest.weebly.com/).
- Not every part of the map will be there when you open it in Java Edition. For example, Tumble maps won't have the spleef floors since the floors are dynamically generated depending on the game mode.
- Item Frames just disappear after conversion. This is probably because they're blocks in Legacy Console Edition but entities in Java Edition. You're going to have to check in game where the Item Frames are supposed to be and manually put them in.
- There are some blocks that have weird metadata. In Legacy Console Edition, they appear to work fine and usually just appear as the default metadata for the block. However, when opened in Java Edition, they get converted to air. So you'll end up with some random missing blocks if you don't fix them.
- In 1.12, floating liquids won't flow unless they receive a block update. In 1.13, water can update itself when the chunk loads. So some maps may get ruined by water flowing everywhere.
- MCC Tool Chest appears to convert the maps to a version around 1.11. I'm basing this off the fact that the program knows about blocks introduced in 1.11, but not blocks introduced in 1.12. Even so, maps with 1.12 blocks can still be opened and converted - you just can't view the blocks in the MCC Tool Chest block editor.  
Unfortunately, some maps released late in the development of Wii U edition (such as the Nightmare Before Christmas map, the last DLC map to be added) don't work. The world file can open in MCC Tool Chest, but the chunks themselves can't. They also fail to be converted. I don't know why. I also haven't tested every map.
- In regards to Mini game maps:  
Update Aquatic (1.13) was addded in Patch 38 - September 11th 2018.  
The last Battle maps were added in Patch 18 - February 28th 2017.  
The last Tumble maps were added in Patch 30 - December 19th 2017.  
The last Glide maps were added in Patch 27 - August 29th 2017.  
Since all Mini game maps were released before the flattening, there shouldn't be any major issues converting them to Java Edition. All ids should be converted with the datafixer.
- If you want to bring a map to 1.13+, make sure to open the world and load all the chunks in 1.12 at least once first. Otherwise you may end up with chunks that don't load and softlock the server.

### Tips
- Sometimes the world spawn can be pretty far from where the map itself is built. One way to find the map is to use the the "Find Entity" tool in MCC Tool Chest to search for entities/tile entities that are in the map, such as paintings or chests.

