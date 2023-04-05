from consolemenu import ConsoleMenu, SelectionMenu, MultiSelectMenu, MenuFormatBuilder, PromptUtils, Screen, items, clear_terminal
from consolemenu.items import CommandItem, ExitItem, ExternalItem, FunctionItem, MenuItem, SelectionItem, SubmenuItem
from ichor.cli.menu_description import MenuDescription

ANALYSIS_MENU_DESCRIPTION = MenuDescription("Analysis Menu", subtitle="Use this to do analysis of data with ichor.")
analysis_menu = ConsoleMenu(ANALYSIS_MENU_DESCRIPTION.title, ANALYSIS_MENU_DESCRIPTION.subtitle)
