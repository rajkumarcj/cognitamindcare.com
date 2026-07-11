function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = {};

  if (e.postData && e.postData.contents) {
    e.postData.contents.split('&').forEach(function (pair) {
      var parts = pair.split('=');
      data[decodeURIComponent(parts[0])] =
        decodeURIComponent((parts[1] || '').replace(/\+/g, ' '));
    });
  }

  var nextRow = sheet.getLastRow() + 1;
  sheet.getRange(nextRow, 4).setNumberFormat('@STRING@');

  sheet.getRange(nextRow, 1, 1, 6).setValues([[
    new Date(),
    data.name    || '',
    data.email   || '',
    data.phone   || '',
    data.service || '',
    data.message || ''
  ]]);

  MailApp.sendEmail({
    to: 'cognitamindcare@gmail.com',
    subject: 'New Enquiry: ' + (data.name || 'Anonymous') + ' — ' + (data.service || 'General'),
    body:
      'Name: ' + (data.name || '-') +
      '\nEmail: ' + (data.email || '-') +
      '\nPhone: ' + (data.phone || '-') +
      '\nService: ' + (data.service || '-') +
      '\nMessage: ' + (data.message || '-')
  });

  return ContentService
    .createTextOutput(JSON.stringify({ result: 'success' }))
    .setMimeType(ContentService.MimeType.JSON);
}
