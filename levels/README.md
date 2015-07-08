Dungeon files are formatted as follows:

- wave descriptor list
  - a literal python list, containing one or more wave descriptors
  - wave descriptors are a tuple of (monster_name, count, interval)
  - interval is seconds between monster spawns

    Example:

        [(Dwarf, 10, 1), (Orc, 2, 5)]

- a series of lines of text where each character is a grid cell in the
  dungeon
  - 'dot' (.) is an empty, lit square
  - 'less-than' (<) is where monsters spawn (i.e. stairs coming from
    above, into this dungeon)
  - 'greater-than' (>) is where monsters are headed -- player's "base"
    (i.e. stairs going down into the next dungeon)
  - 'hash' (#) is a solid wall
