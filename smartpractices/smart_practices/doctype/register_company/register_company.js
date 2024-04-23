// Copyright (c) 2024, KAINOTOMO PH LTD and contributors
frappe.ui.form.on("Register Company", {
    refresh(frm) {
        if (!frm.doc.__islocal) {
            frm.set_df_property('declaration_acceptance', 'options', '<p>I/We the undersigned, being the Ultimate Beneficial Owner(s) the of the company <b>' + frm.doc.implemented_from + '</b> by signing this form declare that the information given hereunder and, in the documents, requested hereby is to the best of my/our knowledge true and accurate as the date hereof.</p>');
            frm.set_df_property('ack_notice', 'options', 
            '<p><b>' + frm.doc.implemented_from + '</b> (term which includes its every time subsidiaries and other connected companies), herein called “<b>' + frm.doc.implemented_from + '</b>”, may collect, process, store and transfer any personal data related to you in accordance of the applicable Processing of Personal Data Protection Laws. </p>'
            + '<p>Data includes information relating to you which has been given or shall be given to <b>' + frm.doc.implemented_from + '</b> to carry out its internal due diligence process, client acceptance or engagement procedures, in reference to applicable legal and/or regulatory requirements or for quality review purposes: </p>'
            + '<p><ul><li>during the submission of applications and any other documents</li>'
            + '<li>has been extracted through the execution of your instructions and in general through services rendered to you by <b>' + frm.doc.implemented_from + '</b>. </li></ul></p>'
            + '<p>Processing includes the collection, recording, organization, maintenance, storage, amendment, extraction, use, transfer, transmission or any other form of distribution, the correlation or the combination, the linking, locking, deletion and destruction of the data. </p>'
            + '<p><b>' + frm.doc.implemented_from + '</b> shall maintain, archives, electronic or other, and shall process the data for the purpose of supporting, promoting and servicing our business relationship which includes but is not limited to the provision of corporate services, bank introduction for the opening of bank accounts and bank accounts operation services, and in general corporate legal and business consultancy services.</p>'
            + '<p>Your data may be processed for the purpose of provision of services by <b>' + frm.doc.implemented_from + '</b> through post and/or telephone and/or internet and/or otherwise.</p>'
            + '<p>In addition to the above, please note that the processing of personal data may involve its transfer outside of the European Economic Area (EEA) to third countries where the level of protection is not as adequate as within the EEA. We will ensure that the transfer of personal data is not as adequate as within the EEA. We will ensure that the transfer of personal data to such third countries will only take place following the implementation of a transfer mechanism as prescribed in applicable legislation.</p>'
            + '<p>We will hold your personal data for the longest of the following periods: a) the period required for the performance of the relevant activity or services; b) any retention period required by law; or c) the end of the period of any litigation and/or investigation by a public authority which arises in respect of the relevant activity and/or the services. Should you and/or <b>' + frm.doc.implemented_from + '</b> choose not to proceed with the proposed engagement, then we will hold your personal data for the longest of: a) any retention period required by law, or b) a period of three (3) months.</p>'
            + '<p>Please note that you have the right of access to and rectification of the data and the right of objection, upon a written application send to <b>' + frm.doc.implemented_from + '</b></p>'
            + '<p>Kindly note that data protection terms will be included in the general business of our Engagement Letter upon our mutual agreement to proceed with the proposed cooperation and any personal data collected pursuant to this letter will be retained for the purpose of currying out our engagement.</p>'
            + '<p>Your Sincerely,</p>'
            + '<p><b>' + frm.doc.implemented_from + '</b></p>'
            + '<p></p>'
            + '<p>I hereby acknowledge that I have fully read and understood the content of this letter.</p>'
        );
        }
    },
});
