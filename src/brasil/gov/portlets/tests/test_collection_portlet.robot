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
${title_sample}  Portal Padrao Colecao
${collection_field_id}  form.collection

*** Test cases ***

Test Collection Portlet
    Enable Autologin as  Site Administrator
    Go to Homepage
    Sleep  1s  Wait for overlay

    Manage Portlets
    Add Right Portlet  Portal Padrao Colecao
    Sleep  1s  Wait for overlay

    Page Should Contain Element  id=${title_field_id}
    Input Text  id=${title_field_id}  ${title_sample}

    Select Collection  ${collection_field_id}  News Collection

    Save Portlet
    Sleep  1s  Wait for overlay

    Hide Right Portlet
    Go to Homepage
    Sleep  1s  Wait for overlay

        
