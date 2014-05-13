*** Settings ***

Resource  portlet.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${image_selector}  .ui-draggable .contenttype-image
${link_selector}  .ui-draggable .contenttype-link
${news_item_selector}  .ui-draggable .contenttype-news-item
${file_selector}  .ui-draggable .contenttype-file
${tile_selector}  div.tile-container div.tile
${title_other_sample}  This text should never be saved
${edit_link_selector}  a.edit-tile-link

${title_field_id}  form.header
${title_sample}  Some text for title
${collection_field_id}  form.collection

*** Test cases ***

Test Collection Portlet
    Enable Autologin as  Site Administrator
    Go to Homepage
    Manage Portlets
    Add Right Portlet  Portal Padrao Colecao

    Page Should Contain Element  id=${title_field_id}
    Input Text  id=${title_field_id}  ${title_sample}

    Page Should Contain Element  id=${collection_field_id}
    Input Text  id=${collection_field_id}  News Collection
    Click Button  name=form.collection.search
    Wait Until Page Contains element  name=form.collection.update
    Click Element  css=#formfield-form-collection input[type=radio]
    Click Button  Save
    Wait Until Page Contains element  css=.portlets-manager
    Go to Homepage
