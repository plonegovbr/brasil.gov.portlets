*** Settings ***

Resource  portlet.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${title_field_id}  form.header
${title_sample}  Portal Padrao Colecao
${titleurl_field_id}  form.header_url
${titleurl_sample}  http://www.plone.org
${imgcheck_field_id}  form.show_image
${collection_field_id}  form.collection

*** Test cases ***

Test Collection Portlet
    Enable Autologin as  Site Administrator
    Go to Homepage
    Sleep  1s  Wait for overlay

    Add Right Portlet  Portal Padrao Colecao
    Page Should Contain Element  id=${title_field_id}
    Input Text  id=${title_field_id}  ${title_sample}
    Select Collection  ${collection_field_id}  News Collection
    Save Portlet
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Page Should Contain Element  id=${titleurl_field_id}
    Input Text  id=${titleurl_field_id}  ${titleurl_sample}
    Save Portlet
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select Checkbox  id=${imgcheck_field_id}
    Save Portlet
    Sleep  1s  Wait for overlay

    Hide Right Portlet
    Go to Homepage
    Sleep  1s  Wait for overlay

    Show Right Portlet
    Go to Homepage
    Sleep  1s  Wait for overlay

    Delete Right Portlet
    Go to Homepage
    Sleep  1s  Wait for overlay
        
    Add Left Portlet  Portal Padrao Colecao
    Page Should Contain Element  id=${title_field_id}
    Input Text  id=${title_field_id}  ${title_sample}
    Select Collection  ${collection_field_id}  News Collection
    Save Portlet
    Sleep  1s  Wait for overlay

    Delete Left Portlet
    Go to Homepage
    Sleep  1s  Wait for overlay
