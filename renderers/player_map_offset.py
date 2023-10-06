def player_map_offset(player, map) -> int:
    if player.x < 10:
        offset = 0
    elif player.x + 50 > map.width:
        offset = map.width - 59
    else:
        offset = player.x - 10

    return offset