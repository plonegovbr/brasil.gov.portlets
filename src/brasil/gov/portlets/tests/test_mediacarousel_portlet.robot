*** Settings ***

Resource  portlet.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${portletname_sample}  Portal Padrao Carrossel de Imagens
${title_field_id}  form.header
${titleurl_field_id}  form.header_url
${titleurl_sample}  http://www.plone.org
${imgcheck_field_id}  form.show_image
${imgsize_field_id}  form.image_size
${imgsize_sample}  mini 200:200
${titletype_field_id}  form.title_type
${titletype_sample}  H4
${footercheck_field_id}  form.show_footer
${footer_field_id}  form.footer
${footer_sample}  More...
${footerurl_field_id}  form.footer_url
${footerurl_sample}  http://www.google.com
${limit_field_id}  form.limit
${limit_sample}  2
${datecheck_field_id}  form.show_date
${dateformat_field_id}  form.date_format
${dateformat_sample}  longa: Data/Hora
${titletype_field_id}  form.title_type
${collection_field_id}  form.collection

*** Test cases ***

Test MediaCarousel Portlet
    Enable Autologin as  Site Administrator
    Go to Homepage
    Sleep  1s  Wait for overlay

    # news collection should get order 2 3 1
    Add Right Portlet  ${portletname_sample}
    Select Collection  ${collection_field_id}  Images Collection
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    Hide Right Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    Show Right Portlet
    Go to Homepage
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    Delete Right Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    # events collection should get order 3 2 1
    Add Left Portlet  ${portletname_sample}
    Select Collection  ${collection_field_id}  Images Collection
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    Delete Left Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay
