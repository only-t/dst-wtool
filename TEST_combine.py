import base64

world_size = 61

separated = open("C:/Users/lukas/OneDrive/Pulpit/usable_tiles.txt", "r")
void = separated.readline().strip()
ocean = separated.readline().strip()
filler = separated.readline().strip()
separated.close()

combined = open("C:/Users/lukas/OneDrive/Pulpit/tiles_combined.txt", "w")
encoded = open("C:/Users/lukas/OneDrive/Pulpit/tiles_encoded.txt", "w")

for row in range(1, world_size + 1):
    for column in range(1, world_size + 1):
        if row == 1 or row == world_size:
            combined.write(void)
        elif row == 2 or row == world_size - 1:
            if column == 1 or column == world_size:
                combined.write(void)
            else:
                combined.write(ocean)
        else:
            if column == 1 or column == world_size:
                combined.write(void)
            elif column == 2 or column == world_size - 1:
                combined.write(ocean)
            else:
                combined.write(filler)

combined.close()

combined = open("C:/Users/lukas/OneDrive/Pulpit/tiles_combined.txt", "r")
encoded.write(str(base64.b64encode(combined.readline().encode("utf-8")), "utf-8"))
combined.close()
encoded.close()
