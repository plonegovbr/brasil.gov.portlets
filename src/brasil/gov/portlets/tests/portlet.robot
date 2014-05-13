*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

*** Variables ***

${PORT} =  55001
${ZOPE_URL} =  http://localhost:${PORT}
${PLONE_URL} =  ${ZOPE_URL}/plone
${BROWSER} =  Firefox

${title_selector} =  input#form-widgets-IBasic-title
${description_selector} =  textarea#form-widgets-IBasic-description
${layout_selector} =  select#form-widgets-template_layout

${row_button_selector} =  a#btn-row
${column_button_selector} =  a#btn-column
${tile_button_selector} =  a#btn-tile
${row_drop_area_selector} =  div.layout
${column_drop_area_selector} =  div.cover-row
${tile_drop_area_selector} =  div.cover-column
${tile_cancel_area_selector} =  div.modal-backdrop
${delete_tile_selector} =  button.close
${CONTENT_CHOOSER_SELECTOR} =  div#contentchooser-content-search

*** Keywords ***

Manage Portlets
    Go to   ${PLONE_URL}/@@manage-portlets

Add Left Portlet
    [arguments]  ${portlet}
    Select from list  xpath=//div[@id="portletmanager-plone-leftcolumn"]//select  ${portlet}
    Wait Until Page Contains element  name=form.actions.save

Add Right Portlet
    [arguments]  ${portlet}
    Select from list  xpath=//div[@id="portletmanager-plone-rightcolumn"]//select  ${portlet}
    Wait Until Page Contains element  name=form.actions.save

Edit Left Portlet
    [arguments]  ${portlet}
    Open Action Menu
    Click Link  css=a#delete
    Click Button  Delete
    Page Should Contain  Plone site

Edit Right Portlet
    [arguments]  ${portlet}
    Click Link  ${portlet}

Delete Left Portlet
    [arguments]  ${portlet}
    Open Action Menu
    Click Link  css=a#delete
    Click Button  Delete
    Page Should Contain  Plone site

Delete Right Portlet
    [arguments]  ${portlet}
    Open Action Menu
    Click Link  css=a#delete
    Click Button  Delete
    Page Should Contain  Plone site
