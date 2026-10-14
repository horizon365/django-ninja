# 996 Salary Calculator

Page: https://georgehuan1994.github.io/996-Salary-Calculator/

## परिचय

<br/>

> "आपकी अपेक्षित (expected) salary क्या है?"

<br/>

यह लगभग एक अनिवार्य सवाल है।

ज़्यादातर लोगों की अपेक्षित salary एक बड़ी range होती है, और यह अलग-अलग कंपनियों और departments में काफ़ी भिन्न होती है।

उदाहरण के लिए: working hours क्या हैं? क्या overtime pay मिलता है? 14 महीनों की salary? 16 महीनों की salary? Housing provident fund? Base salary?

...

इसलिए बताई गई salary अक्सर बहुत subjective और arbitrary होती है।

और इसीलिए यह tool मौजूद है!

---

Click करके यहाँ जाएँ: [996 Salary Calculator](https://georgehuan1994.github.io/996-Salary-Calculator/)

![2021-10-15_115036](https://user-images.githubusercontent.com/49583943/137430292-c785dbb0-ea57-4989-862f-46cd2e860500.png)

## व्याख्या

### Expected Annual Salary

"965 schedule, 12 महीनों की salary, full housing provident fund" के standard के आधार पर, अपनी अपेक्षित annual salary enter करें और standard hourly rate तथा standard monthly salary पाएँ।

### Daily Working Hours

Presets: 965, 995, 995.5, 996। Custom working hours भी support किए जाते हैं, जैसे Tencent का Wednesday Health Day।

पूरे साल (50 weeks) के regular working hours, overtime hours और rest-day hours की गणना करता है, और फिर प्राप्त होने वाली (entitled) annual salary तथा entitled monthly salary निकालता है।

- किसी workday के पहले 9 hours को hourly rate के 1x पर **regular hours** गिना जाता है;
- किसी workday में 9 से अधिक hours को hourly rate के 1.5x पर **overtime hours** गिना जाता है;
- किसी rest day में 0 से अधिक hours को hourly rate के 2x पर **rest-day hours** गिना जाता है।

### Annual Payout

वे महीने enter करें जिनके दौरान salary दी जाती है। 12 महीने? 13.5 महीने? 14 महीने? 16 महीने? ...

### Housing Provident Fund Contribution Rate (Company)

निचली सीमा: 5%, ऊपरी सीमा: 12%

कई लोगों की कंपनी के housing provident fund contribution rate को लेकर एक भ्रांति होती है, यानी: "जो मैं contribute करूँगा, वही कंपनी भी contribute करेगी।"

लेकिन यह value व्यक्ति द्वारा चुनी गई rate से संबंधित नहीं है। कंपनियाँ आम तौर पर एक fixed rate चुनती हैं और व्यक्ति की contribution rate का पालन नहीं करतीं।

### Housing Provident Fund Contribution Base (Company)

निचली सीमा: 2100, ऊपरी सीमा: 33786। क्षेत्रों के बीच कुछ अंतर है।

कई कंपनियों में न केवल contribution rate कम होता है, बल्कि contribution base भी कम होता है।

**महत्वपूर्ण बात: यह value आम तौर पर labor contract के "base salary" के साथ consistent होती है। Disputes, layoffs, या non-compete agreements से संबंधित compensation इससे प्रभावित हो सकता है!**

### Adjusted Monthly Salary

Housing provident fund contribution rate और base के आधार पर, entitled monthly salary को adjust करें।

---

    अगर यह project आपकी मदद करता है, तो ऊपरी दाएँ कोने में star button पर click करें और मुझे एक Star ⭐️ देकर हौसला बढ़ाएँ~
