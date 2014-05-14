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
    Click Link  css=#portletmanager-plone-leftcolumn .portletHeader>a
    Wait Until Page Contains element  name=form.actions.save

Edit Right Portlet
    Click Link  css=#portletmanager-plone-rightcolumn .portletHeader>a
    Wait Until Page Contains element  name=form.actions.save

Delete Left Portlet
    Click Element  css=#portletmanager-plone-leftcolumn .delete button

Delete Right Portlet
    Click Element  css=#portletmanager-plone-rightcolumn .delete button

Hide Left Portlet
    Click Element  css=#portletmanager-plone-leftcolumn .portlet-action:nth-child(1) button

Hide Right Portlet
    Click Element  css=#portletmanager-plone-rightcolumn .portlet-action:nth-child(1) button

Select Collection
    [arguments]  ${collection_field_id}  ${collection_name}
    Page Should Contain Element  id=${collection_field_id}
    Input Text  id=${collection_field_id}  ${collection_name}
    Click Button  name=${collection_field_id}.search
    Wait Until Page Contains element  name=${collection_field_id}.update
    Click Element  xpath=//div[@data-fieldname='${collection_field_id}']//input[@type='radio'][@name='${collection_field_id}']
    
Save Portlet
    Click Button  Save
    Wait Until Page Contains element  css=.portlets-manager
    Go to Homepage

Cancel Portlet
    Click Button  Cancel
    Wait Until Page Contains element  css=.portlets-manager
    Go to Homepage
