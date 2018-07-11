from block import Block, random_init
from goal import BlobGoal
from renderer import COLOUR_LIST


def test_rectangles_to_draw():
    """
    Tests the rectangles to draw method.
    """
    # Compute the rectangles for this hard-coded example.
    # Convert to a set, since no particular rectangle order was required.
    block = Block(0, children=[
        Block(1, children=[
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2])
        ])
    ])
    block.update_block_locations((0, 0), 50)
    actual_set = set(block.rectangles_to_draw())

    # Define the correct set of rectangles, again as a set.
    correct_rectangles = [((138, 151, 71), (37, 0), (12, 12), 0),
                          ((0, 0, 0), (37, 0), (12, 12), 3),
                          ((199, 44, 58), (25, 0), (12, 12), 0),
                          ((0, 0, 0), (25, 0), (12, 12), 3),
                          ((138, 151, 71), (25, 12), (12, 12), 0),
                          ((0, 0, 0), (25, 12), (12, 12), 3),
                          ((1, 128, 181), (37, 12), (12, 12), 0),
                          ((0, 0, 0), (37, 12), (12, 12), 3),
                          ((1, 128, 181), (12, 0), (12, 12), 0),
                          ((0, 0, 0), (12, 0), (12, 12), 3),
                          ((199, 44, 58), (0, 0), (12, 12), 0),
                          ((0, 0, 0), (0, 0), (12, 12), 3),
                          ((199, 44, 58), (0, 12), (12, 12), 0),
                          ((0, 0, 0), (0, 12), (12, 12), 3),
                          ((138, 151, 71), (12, 12), (12, 12), 0),
                          ((0, 0, 0), (12, 12), (12, 12), 3),
                          ((138, 151, 71), (12, 25), (12, 12), 0),
                          ((0, 0, 0), (12, 25), (12, 12), 3),
                          ((199, 44, 58), (0, 25), (12, 12), 0),
                          ((0, 0, 0), (0, 25), (12, 12), 3),
                          ((199, 44, 58), (0, 37), (12, 12), 0),
                          ((0, 0, 0), (0, 37), (12, 12), 3),
                          ((1, 128, 181), (12, 37), (12, 12), 0),
                          ((0, 0, 0), (12, 37), (12, 12), 3),
                          ((1, 128, 181), (37, 25), (12, 12), 0),
                          ((0, 0, 0), (37, 25), (12, 12), 3),
                          ((138, 151, 71), (25, 25), (12, 12), 0),
                          ((0, 0, 0), (25, 25), (12, 12), 3),
                          ((199, 44, 58), (25, 37), (12, 12), 0),
                          ((0, 0, 0), (25, 37), (12, 12), 3),
                          ((138, 151, 71), (37, 37), (12, 12), 0),
                          ((0, 0, 0), (37, 37), (12, 12), 3)]
    correct_set = set(correct_rectangles)

    # There must be no difference between the actual set and the correct set!
    assert actual_set.difference(correct_set) == set()
    assert correct_set.difference(actual_set) == set()


# def test_get_block():
#     block = Block(0, children=[
#         Block(1, children=[
#             Block(2, COLOUR_LIST[2]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[2]),
#             Block(2, COLOUR_LIST[0])
#         ]),
#         Block(1, children=[
#             Block(2, COLOUR_LIST[0]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[2])
#         ]),
#         Block(1, children=[
#             Block(2, COLOUR_LIST[2]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[0])
#         ]),
#         Block(1, children=[
#             Block(2, COLOUR_LIST[0]),
#             Block(2, COLOUR_LIST[2]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[2])
#         ])
#     ])
#     block.update_block_locations((0, 0), 750)
#     b = block.get_selected_block((282, 563), 2)
#     b2 = block.get_selected_block((0, 375), 1)
#     b3 = block.get_selected_block((0, 0), 0)
#     b4 = block.get_selected_block((375, 0), 1)
#     b5 = block.get_selected_block((188, 375), 2)
#     b6 = block.get_selected_block((375, 375), 1)
#     assert block.position == (0, 0)
#     assert block.size == 750
#     assert block.children[2].children[0].position == (188, 375)
#     assert b == block.children[2].children[0]
#     assert b3 == block
#     assert b4.position == block.children[0].position
#     assert b2.position == block.children[2].position
#     assert b5.position == block.children[2].children[0].position
#     assert b6.position == block.children[3].position

# def test_flatten():
#     # block = Block(0, children=[
#     #     Block(1, COLOUR_LIST[2]),
#     #     Block(1, COLOUR_LIST[1]),
#     #     Block(1, COLOUR_LIST[2]),
#     #     Block(1, COLOUR_LIST[0])
#     # ])
#     block = Block(0, children=[
#         Block(1, COLOUR_LIST[0]),
#         Block(1, children=[
#             Block(2, COLOUR_LIST[0]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[2])
#         ]),
#         Block(1, children=[
#             Block(2, COLOUR_LIST[2]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[0])
#         ]),
#         Block(1, children=[
#             Block(2, COLOUR_LIST[0]),
#             Block(2, COLOUR_LIST[2]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[2])
#         ])
#     ])
#     # b = random_init(0, 3)
#     # b.update_block_locations((0, 0), 750)
#     block.update_block_locations((0, 0), 750)
#     block.max_depth = 2
#     for child in block.children:
#         child.max_depth = 2
#     for child in block.children[0].children:
#         child.max_depth = 2
#     for child in block.children[1].children:
#         child.max_depth = 2
#     for child in block.children[2].children:
#         child.max_depth = 2
#     for child in block.children[3].children:
#         child.max_depth = 2
#     b = block.flatten()
#     # b1 = b.flatten()
#     print(b)
#     # assert b[0][0] == block.children[1].children[1].colour
#     assert b[0][0] == block.children[1].children[1].colour
#     assert b[1][0] == block.children[0].colour
#
#
# def test_rotate():
#     block = Block(0, children=[
#         Block(1, COLOUR_LIST[0]),
#         Block(1, children=[
#             Block(2, COLOUR_LIST[0]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[2])
#         ]),
#         Block(1, children=[
#             Block(2, COLOUR_LIST[2]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[0])
#         ]),
#         Block(1, children=[
#             Block(2, COLOUR_LIST[0]),
#             Block(2, COLOUR_LIST[2]),
#             Block(2, COLOUR_LIST[1]),
#             Block(2, COLOUR_LIST[2])
#         ])
#     ])
#     block.update_block_locations((0, 0), 750)
#     block.max_depth = 2
#     for child in block.children:
#         child.max_depth = 2
#     for child in block.children[0].children:
#         child.max_depth = 2
#     for child in block.children[1].children:
#         child.max_depth = 2
#     for child in block.children[2].children:
#         child.max_depth = 2
#     for child in block.children[3].children:
#         child.max_depth = 2
#     b = block.flatten()
#     block.rotate(1)
#     b1 = block.flatten()
#     print(b1)
#     expected = [[COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1]],
#                 [COLOUR_LIST[0], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[0]],
#                 [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[0], COLOUR_LIST[0]],
#                 [COLOUR_LIST[2], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0]]]
#     assert expected == b1


# def test_blob_size():
#     block = Block(0, children=[
#             Block(1, children=[
#                 Block(2, COLOUR_LIST[1]),
#                 Block(2, COLOUR_LIST[3]),
#                 Block(2, COLOUR_LIST[1]),
#                 Block(2, COLOUR_LIST[3])
#             ]),
#             Block(1, children=[
#                 Block(2, COLOUR_LIST[0]),
#                 Block(2, COLOUR_LIST[2]),
#                 Block(2, COLOUR_LIST[1]),
#                 Block(2, COLOUR_LIST[0])
#             ]),
#             Block(1, children=[
#                 Block(2, COLOUR_LIST[1]),
#                 Block(2, COLOUR_LIST[0]),
#                 Block(2, COLOUR_LIST[1]),
#                 Block(2, COLOUR_LIST[1])
#             ]),
#             Block(1, children=[
#                 Block(2, COLOUR_LIST[3]),
#                 Block(2, COLOUR_LIST[2]),
#                 Block(2, COLOUR_LIST[3]),
#                 Block(2, COLOUR_LIST[3])
#             ])
#         ])
#     block.update_block_locations((0, 0), 750)
#     block.max_depth = 1
#     for child in block.children:
#         child.max_depth = 1
#     for child in block.children[0].children:
#         child.max_depth = 2
#     for child in block.children[1].children:
#         child.max_depth = 2
#     for child in block.children[2].children:
#         child.max_depth = 2
#     for child in block.children[3].children:
#         child.max_depth = 2
#     b = block.flatten()
#     goal = BlobGoal(COLOUR_LIST[3])
#     visited = [[-1 for _ in range(len(b))]
#                for _ in range(len(b))]
#     print(b)
#     print(visited)
#     lst_blob_size = []
#     for i in range(len(b)):
#         for j in range(len(b)):
#             lst_blob_size.append(
#                 goal._undiscovered_blob_size((i, j), b, visited))
#     print(lst_blob_size)
#     assert max(lst_blob_size) == 4
