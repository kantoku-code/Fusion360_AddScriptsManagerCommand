# FusionAPI_python addin
# Author-kantoku
# Description-add ScriptsManagerCommand at Render and Draw

import traceback
import adsk.core as core

HEADER = "kantoku"

TARGET_WORKSPACE_IDS = (
    "FusionRenderEnvironment",
    "FusionDocumentationEnvironment",
)
COMMAND_IDS = (
    "ScriptsManagerCommand",
    "ExchangeAppStoreCommand",
)

_removeItems = []

def run(context):
    ui: core.UserInterface = None
    try:
        app: core.Application = core.Application.get()
        ui = app.userInterface

        refDict = get_ref_tab_panel()
        defs = get_commandDefinition_list(COMMAND_IDS)
        if len(defs) < 1: return

        global _removeItems
        for wsId in TARGET_WORKSPACE_IDS:
            ws: core.Workspace = ui.workspaces.itemById(wsId)
            if not ws: continue

            tab: core.ToolbarTab = get_tab(
                ws.toolbarTabs,
                f'{HEADER}_{refDict["tab"].id}',
                f'{refDict["tab"].name}',
            )
            _removeItems.append(tab)

            panel: core.ToolbarPanel = get_panel(
                tab.toolbarPanels,
                f'{HEADER}_{refDict["panel"].id}',
                f'{refDict["panel"].name}',
            )
            _removeItems.append(panel)

            register_command(
                panel,
                defs,
            )

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    global _removeItems
    for item in reversed(_removeItems):
        try:
            item.deleteMe()
        except:
            pass


def get_commandDefinition_list(
    ids: tuple[str],
) -> list[core.CommandDefinition]:

    app: core.Application = core.Application.get()
    ui: core.UserInterface = app.userInterface

    defs = []
    for id in ids:
        cmdDef: core.CommandDefinition = ui.commandDefinitions.itemById(
            id
        )
        if cmdDef:
            defs.append(cmdDef)

    return defs


def register_command(
    panel: core.ToolbarPanel,
    defs: list[core.CommandDefinition],
) -> None:

    cmdDef: core.CommandDefinition = None
    for cmdDef in defs:
        control :core.ToolbarControl = panel.controls.itemById(cmdDef.id)
        if control: control.deleteMe()

        control :core.ToolbarControl = panel.controls.addCommand(
            cmdDef
        )
        control.isVisible = True
        control.isPromoted = True
        control.isPromotedByDefault = True


def get_panel(
    panels: core.ToolbarPanels,
    id: str,
    name: str,
) -> core.ToolbarPanel:

    panel: core.Toolbarpanel = panels.itemById(id)
    if not panel:
        panel = panels.add(
            id,
            name,
        )

    return panel


def get_tab(
    tabs: core.ToolbarTabs,
    id: str,
    name: str,
) -> core.ToolbarTab:

    tab: core.ToolbarTab = tabs.itemById(id)
    if not tab:
        tab = tabs.add(
            id,
            name,
        )

    return tab


def get_ref_tab_panel(
) -> dict:

    app: core.Application = core.Application.get()
    ui: core.UserInterface = app.userInterface

    tab: core.ToolbarTab = ui.toolbarTabsByProductType(
        'DesignProductType'
    ).itemById('ToolsTab')

    panel: core.ToolbarPanel = tab.toolbarPanels.itemById(
        'SolidScriptsAddinsPanel'
    )

    return {
        'tab': tab,
        'panel': panel,
    }