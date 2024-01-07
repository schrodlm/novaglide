import pytest
import sys
import pygame
from match.elo import Elo
from match.match_stats import MatchStats, MatchStatsData
from game_objects.player import Player
from menu_elements.table import Table
from menu_elements.button import Button
from menu_elements.input_box import InputBox
from configuration_mod import Config
from custom_exceptions import InvalidColorString, OutOfBoundsError
from unittest.mock import Mock
import utilities
pygame.init()
screen = pygame.display.set_mode(
[340,300], pygame.HWSURFACE, 32)

@pytest.mark.parametrize("elo_1, elo_2, winner, expected",[(500,500,True,(528, 472)),
    (0,8000,False,(-208, 8208)),
    (300,250,True,(344, 206)),
    (200,6489,True,(374, 6315)),
    (4,250,True,(54, 200)),
    (6800,8000,True,(6871, 7929)),
    (1000,400,True,(1058, 342))])
def test_elo_result(elo_1, elo_2, winner, expected):
    assert expected == Elo.calculate_elo(elo_1, elo_2, winner)

@pytest.mark.parametrize("elo_1, elo_2, winner",[("a",500,False),
    (3,3,"string"),
    (["a"],250,True),
    (200,6489,["a"]),
    (4,["a"],True)])
def test_elo_constructor(elo_1, elo_2, winner):
    if type(elo_1) != int or type(elo_2) != int:
        with pytest.raises(TypeError) as exc_info:
            Elo.calculate_elo(elo_1, elo_2, winner)
        assert str(exc_info.value) == "Both player elos need to be integers"
    else:
        if type(winner) == bool:
            with pytest.raises(ValueError) as exc_info:
                Elo.calculate_elo(elo_1, elo_2, winner)
            assert str(exc_info.value) =="Winner has to be true or false"

def test_match_stats_constructor():
    config = Config()
    config = config.config
    player = Player("",3,4,config, 59,server=True)
    group_1 = pygame.sprite.Group()
    stats = MatchStats([player])
    assert stats.stats[""]["touches"] == 0
    with pytest.raises(TypeError) as exc_info:
        MatchStats([Player("",3,4,config, 59,server=True),3])
    assert str(exc_info.value) == "Entities must be Player or Ball"

def test_match_stats_data_constructor():
    config = Config()
    config = config.config
    player = Player("",3,4,config, 59,server=True)
    group_1 = pygame.sprite.Group()
    stats = MatchStats([player])
    with pytest.raises(TypeError) as exc_info:
        MatchStatsData(stats.stats,player)
    assert str(exc_info.value) == "Incorrect type of input parameters"




@pytest.fixture
def create_entities():
    config = Config()
    config = config.config
    player_a = Player("a",3,4,config, 59,server=True)
    player_b = Player("b",3,4,config, 59,server=True)
    player_c = Player("c",3,4,config, 59,server=True)
    group_1 = pygame.sprite.Group()
    group_1.add(player_a)
    group_1.add(player_b)
    group_1.add(player_c)
    yield group_1

def test_set_add_stats(create_entities):
    match_stats = MatchStats(create_entities)
    for entity in create_entities:
        match_stats.add_touch(entity)
        match_stats.set_elo(entity)
        match_stats.add_goal(entity)
    for entity in create_entities:
        assert 1 == match_stats.stats[entity.name]["touches"]
        assert 59 == match_stats.stats[entity.name]["elo"]
        assert 1 == match_stats.stats[entity.name]["goals"]
        
def test_get_stats(create_entities):
    match_stats = MatchStats(create_entities)
    match_stats.set_winner("a")
    assert MatchStatsData == type(match_stats.get_stats())
    
@pytest.mark.parametrize("text, size, x, y, display, color",[("auto", "b",
                            40, 550, pygame.surface.Surface([1000,1000]),
                            (255,30,25)),
    (4, "b",
                            40, "None", pygame.surface.Surface([1000,1000]),
                            (255,30,25)),
    ("None", "b",
                            40, 550, pygame.surface.Surface([1000,1000]),
                            (255,30,25)),
    ("None", "b",
                            40, 550, pygame.surface.Surface([1000,1000]),
                            (255,30,25)),
    ("auto", "b",
                            40, 550, pygame.surface.Surface([1000,1000]),
                            (255,30,25)),
    ])
def test_draw_text(text, size, x, y, display, color):
    with pytest.raises(TypeError) as exc_info:
        utilities.draw_text(text, size, x, y, display, color)
    assert str(exc_info.value) == "Incorrect type of the parameters."
    
def test_draw_text_valid_input():
    display = pygame.Surface((800, 600))
    utilities.draw_text("Hello", 20, 400, 300, display)


def test_draw_text_invalid_type():
    display = pygame.Surface((800, 600))
    with pytest.raises(TypeError):
        utilities.draw_text("Hello", "20", 400, 300, display)

def test_draw_text_invalid_color():
    display = pygame.Surface((800, 600))
    with pytest.raises(ValueError):
        utilities.draw_text("Hello", 20, 400, 300, display, color="invalid_color")

def test_get_image_valid_input():
    image = utilities.get_image("back_arrow")
    assert isinstance(image, pygame.Surface)

def test_get_image_invalid_input():
    with pytest.raises(FileNotFoundError):
        utilities.get_image("nonexistent_image")

@pytest.mark.parametrize("name",["back_arrow", "background_main", "background_ranked", "ranks", "ranks_frames",
                 "left_arrow", "right_arrow", "WOODEN", "IRON", "BRONZE", "SILVER", "GOLD", "CHALLENGER"])
def test_get_image_all_images_exist(name):
    image = utilities.get_image(name)
    assert isinstance(image, pygame.Surface)
@pytest.mark.parametrize("volume, expected",[(0, "0 %"), (1, "10 %"), (2, "20 %"), (3, "30 %"), (4, "40 %"),
             (5, "50 %"), (6, "60 %"), (7, "70 %"), (8, "80 %"), (9, "90 %"),
             (10, "100 %")])
def test_convert_volume_valid_input(volume, expected):
    assert utilities.convert_volume(volume) == expected

def test_convert_volume_invalid_input():
    with pytest.raises(ValueError):
        utilities.convert_volume(-1)

    with pytest.raises(ValueError):
        utilities.convert_volume(11)

def test_convert_volume_type_error():
    with pytest.raises(ValueError):
        utilities.convert_volume("string")

    with pytest.raises(ValueError):
        utilities.convert_volume(3.5)

@pytest.mark.parametrize("map_value, expected_name", [
    ("./../resources/rink_bg_1.jpg", "MAP 1"),
    ("./../resources/rink_bg_2.jpg", "MAP 2"),
    ("./../resources/rink_bg_3.jpg", "MAP 3"),
])
def test_get_map_names_valid_input(map_value, expected_name):
    assert utilities.get_map_names(map_value) == expected_name

@pytest.mark.parametrize("map_value", [
    "./../resources/nonexistent_map.jpg",
    "./../resources/invalid_path.jpg",
    "./../resources/another_invalid_path.jpg",
])
def test_get_map_names_invalid_input(map_value):
    with pytest.raises(KeyError):
        utilities.get_map_names(map_value)
        
@pytest.mark.parametrize("x, y", [
    (100, 200),  
    (0, 0),
    (800, 600),
])
def test_check_inside_screen_valid_coordinates(x, y):
    utilities.check_inside_screen(x, y)

@pytest.mark.parametrize("x, y", [
    (-10, 200),
    (100, -10),
    (1500, 200),
    (-3, 20000),
])
def test_check_inside_screen_invalid_coordinates(x, y):
    with pytest.raises(OutOfBoundsError):
        utilities.check_inside_screen(x, y)
        
def test_check_color_values_valid():
    utilities.check_color_values(100, 150, 200)

def test_check_color_values_invalid_type():
    with pytest.raises(ValueError):
        utilities.check_color_values("red", 150, 200)

def test_check_color_values_invalid_range():
    with pytest.raises(OutOfBoundsError):
        utilities.check_color_values(300, 150, 200)

    with pytest.raises(OutOfBoundsError):
        utilities.check_color_values(100, -50, 200)

    with pytest.raises(OutOfBoundsError):
        utilities.check_color_values(100, 150, 300)
        
def test_valid_color():
    valid_colors = ["red", "green", "blue", "white", "black"]
    for color in valid_colors:
        assert utilities.check_string_color_posibility(color) is None
@pytest.mark.parametrize("color",["purplefgh", "fghyellow", "pifghnk", "browfghn", "grfghay"])
def test_invalid_color(color):
    with pytest.raises(InvalidColorString):
        utilities.check_string_color_posibility(color)

def test_empty_string():
    with pytest.raises(InvalidColorString):
        utilities.check_string_color_posibility("")

def test_whitespace_string():
    with pytest.raises(InvalidColorString):
        utilities.check_string_color_posibility("  ")

def test_mixed_case_color():
    mixed_case_color = "ReD"
    with pytest.raises(InvalidColorString):
        utilities.check_string_color_posibility(mixed_case_color)

@pytest.fixture
def config():
    return {
        "design": {
            "table_lines_colour": "white",
            "table_contents_colour": "aqua"
        },
        "colours": {
            "aqua": "aqua"
        }
    }

def test_table_initialization(config):
    cols_sizes = [100, 150, 200]
    table = Table(config, cols_sizes, header="Test Table", row_size=30, n_rows=5)

    assert isinstance(table, Table)
    assert table.header == "Test Table"
    assert table.row_size == 30
    assert table.top_left_coords == (640, 50)
    assert table.font_size == 16
    assert table.header_font_size == 25
    assert table.n_cols == len(cols_sizes)
    assert table.cols_sizes == cols_sizes
    assert table.n_rows == 5
    assert table.lines_color == "white"
    assert table.contents_color == "aqua"

def test_table_update(config):
    cols_sizes = [100, 150, 200]
    table = Table(config, cols_sizes, header="Test Table", row_size=30, n_rows=5)

    # Create a simple surface object
    display = pygame.Surface((800, 600))

    table.update(display)

def test_table_insert_data(config):
    cols_sizes = [100, 150, 200]
    table = Table(config, cols_sizes, header="Test Table", row_size=30, n_rows=5)

    display = pygame.Surface((800, 600))

    data = ["Data 1", "Data 2", "Data 3", "Data 4", "Data 5",
            "Data 6", "Data 7", "Data 8", "Data 9", "Data 10",
            "Data 11", "Data 12", "Data 13", "Data 14", "Data 15"]
    table.insert_data(data, display)

@pytest.mark.parametrize("image, pos, text_input, font, base_color, hovering_color",
                         [
                             (None, (100, 100), "Click me", "invalid_font", (255, 0, 0), (0, 255, 0)),
                             ("invalid_image", (100, 100), "Click me", None, (255, 0, 0), (0, 255, 0)),
                             (None, "invalid_pos", "Click me", None, (255, 0, 0), (0, 255, 0)),
                             (None, (100, 100), None, None, (255, 0, 0), (0, 255, 0)),
                             (None, (100, 100), "Click me", None, "invalid_base_color", (0, 255, 0)),
                             (None, (100, 100), "Click me", None, (255, 0, 0), "invalid_hovering_color"),
                         ])
def test_button_invalid_inputs(image, pos, text_input, font, base_color, hovering_color):
    with pytest.raises((TypeError, ValueError)):
        button = Button(image, pos, text_input, font, base_color, hovering_color)

@pytest.fixture
def font():
    return utilities.get_font(32)

def test_button_initialization(font):
    pos = (100, 100)
    base_color = (255, 0, 0)
    hovering_color = (0, 255, 0)
    button = Button(None, pos, "Click me", font, base_color, hovering_color)

    assert isinstance(button, Button)
    assert button.x_pos == pos[0]
    assert button.y_pos == pos[1]
    assert button.font == font
    assert button.base_color == base_color
    assert button.hovering_color == hovering_color
    assert button.text_input == "Click me"

def test_button_update(font):
    pos = (100, 100)
    base_color = (255, 0, 0)
    hovering_color = (0, 255, 0)
    button = Button(None, pos, "Click me", font, base_color, hovering_color)

    screen = pygame.Surface((800, 600))

    button.update(screen)

def test_button_check_for_input(font):
    pos = (100, 100)
    base_color = (255, 0, 0)
    hovering_color = (0, 255, 0)
    button = Button(None, pos, "Click me", font, base_color, hovering_color)

    assert not button.check_for_input((50, 50))

    assert button.check_for_input((110, 110))

def test_button_change_color(font):
    pos = (100, 100)
    base_color = (255, 0, 0)
    hovering_color = (0, 255, 0)
    button = Button(None, pos, "Click me", font, base_color, hovering_color)

    button.change_color((50, 50))
    assert button.text.get_at((0, 0))[:3] == base_color
    button.change_color((110, 110))
    assert button.text.get_at((0, 0))[:3] == hovering_color
    
@pytest.fixture
def valid_button():
    font = pygame.font.Font(None, 36)
    return Button(None, (100, 100), "Click me", font, (255, 0, 0), (0, 255, 0))

@pytest.mark.parametrize("screen", ["invalid_screen", 123, 3.14, True])
def test_button_invalid_update(valid_button, screen):
    with pytest.raises(TypeError):
        valid_button.update(screen)

@pytest.mark.parametrize("position", ["invalid_position", (1, "a"), (1, 2, 3), (1.5, 2)])
def test_button_invalid_check_for_input(valid_button, position):
    with pytest.raises((TypeError, ValueError)):
        valid_button.check_for_input(position)

@pytest.mark.parametrize("position", ["invalid_position", (1, "a"), (1, 2, 3), (1.5, 2)])
def test_button_invalid_change_color(valid_button, position):
    with pytest.raises((TypeError, ValueError)):
        valid_button.change_color(position)
        
MOCK_CONFIG = {
    "design": {
        "input_box_inactive_colour": {"r": 255, "g": 0, "b": 0},
        "input_box_active_colour": {"r": 0, "g": 255, "b": 0}
    }
}

@pytest.fixture
def valid_input_box():
    return InputBox(100, 100, 200, 50, False, MOCK_CONFIG)

@pytest.mark.parametrize("x, y, w, h, hide, config, font, text", [
    (100, 100, 200, 50, False, MOCK_CONFIG, pygame.font.Font(None, 32), ""),
    (200, 200, 400, 100, True, MOCK_CONFIG, pygame.font.Font(None, 24), "InitialText"),
    (300, 300, 300, 75, False, MOCK_CONFIG, pygame.font.Font(None, 16), "AnotherText"),
])
def test_input_box_constructor_valid_inputs(x, y, w, h, hide, config, font, text):
    input_box = InputBox(x, y, w, h, hide, config, font=font, text=text)
    assert input_box.hide == hide
    assert input_box.config == config
    assert input_box.font == font
    assert input_box.text == text

@pytest.mark.parametrize("x, y, w, h, hide, config, font, text", [
    ("not_an_integer", 100, 200, 50, False, MOCK_CONFIG, pygame.font.Font(None, 32), ""),
    (100, "not_an_integer", 200, 50, False, MOCK_CONFIG, pygame.font.Font(None, 32), ""),
    (100, 100, "not_an_integer", 50, False, MOCK_CONFIG, pygame.font.Font(None, 32), ""),
    (100, 100, 200, "not_an_integer", False, MOCK_CONFIG, pygame.font.Font(None, 32), ""),
    (100, 100, 200, 50, "not_a_boolean", MOCK_CONFIG, pygame.font.Font(None, 32), ""),
    (100, 100, 200, 50, False, "not_a_dict", pygame.font.Font(None, 32), ""),
    (100, 100, 200, 50, False, MOCK_CONFIG, "not_a_font", ""),
    (100, 100, 200, 50, False, MOCK_CONFIG, pygame.font.Font(None, 32), 42),
])
def test_input_box_constructor_invalid_inputs(x, y, w, h, hide, config, font, text):
    with pytest.raises((TypeError, ValueError)):
        InputBox(x, y, w, h, hide, config, font=font, text=text)

@pytest.mark.parametrize("event", ["invalid_event", 123, 3.14, True])
def test_input_box_invalid_handle_event(valid_input_box, event):
    with pytest.raises(TypeError):
        valid_input_box.handle_event(event)

@pytest.mark.parametrize("text", [123, 3.14, True, ["a", "b"]])
def test_input_box_invalid_init_text(valid_input_box, text):
    with pytest.raises(TypeError):
        InputBox(100, 100, 200, 50, False, MOCK_CONFIG, text=text)

@pytest.mark.parametrize("screen", ["invalid_screen", 123, 3.14, True])
def test_input_box_invalid_draw_updated(valid_input_box, screen):
    with pytest.raises(RuntimeError):
        valid_input_box.draw_updated(screen)
