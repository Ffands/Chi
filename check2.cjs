const https = require('https');
https.get(`https://dl.google.com/dl/android/maven2/com/google/mlkit/text-recognition-chinese/16.0.0/text-recognition-chinese-16.0.0.pom`, (res) => {
    console.log(`Chinese 16.0.0: ${res.statusCode}`);
});
https.get(`https://dl.google.com/dl/android/maven2/com/google/mlkit/master-index.xml`, (res) => {
  let d = '';
  res.on('data', c => d+=c);
  res.on('end', () => console.log(d));
});
