// Tables of contents for the two courses. Each lesson: [number, title, structure, 'search phrase|search phrase|...'].
// The phrases are what a learner should hear in real clips; the site lists every clip that contains any of them.
window.COURSES = {
  book: {
    name: 'คิดเป็นไทย พูดเป็นอังกฤษ',
    volumes: [
      { name: 'เล่ม 1', sections: [
        { name: 'หมวด 1 ตัวฉันและสิ่งรอบตัว', lessons: [
          [1, 'ฉันชื่อดาว อายุ 35 ปี', "My name is … / I'm … years old.", 'my name is|years old'],
          [2, 'ฉันเป็นพยาบาล', 'ประธาน + am/is/are + a/an + อาชีพ', "i'm a|she's a|he's a|i am a"],
          [3, 'เธอใจดี', 'ประธาน + am/is/are + คำคุณศัพท์', "she's very|he's so|you're so|they're really"],
          [4, 'ฉันไม่ยุ่ง / คุณหิวไหม', 'am/is/are + not / Am/Is/Are …?', "i'm not|are you hungry|are you okay|is it"],
          [5, 'ฉันมาจากอุดรธานี ฉันอาศัยอยู่ที่ขอนแก่น', 'from + สถานที่ / live in', "i'm from|i live in|where are you from|we live in"],
          [6, 'นี่คือน้องสาวของฉัน / นี่คือรองเท้าของฉัน', 'this / that / these / those', 'this is my|that is|these are|those are'],
          [7, 'อาหารที่ฉันชอบที่สุดคือส้มตำ', 'My favorite … is …', 'my favorite|my favourite'],
          [8, 'ฉันมีครอบครัวใหญ่', 'have / has', 'i have a|she has a|we have a|he has'],
          [9, 'มีร้านสะดวกซื้ออยู่ใกล้บ้านฉัน', 'There is / There are', "there's a|there is a|there are"],
          [10, 'กุญแจอยู่บนโต๊ะ', 'in / on / under / next to / at', 'on the table|under the|next to the|in the box']
        ]},
        { name: 'หมวด 2 ทำอะไรทุกวัน', lessons: [
          [11, 'ฉันกินข้าวเช้าตอน 7 โมง', 'ประธาน + กริยา + เวลา', "breakfast at|o'clock|in the morning|at night"],
          [12, 'พ่อของฉันทำงานที่ธนาคาร', 'เติม s / es', 'my dad works|she works|he works|my mom'],
          [13, 'ฉันไม่กินหมู', "don't / doesn't", "i don't eat|she doesn't|i don't like|he doesn't"],
          [14, 'คุณชอบสุนัขไหม', 'Do / Does …?', 'do you like|does she|do you have|does he'],
          [15, 'ปกติฉันตื่นนอนตอน 6 โมง', 'always / usually / often / sometimes / never', 'i usually|i always|i never|sometimes i'],
          [16, 'คุณตื่นนอนกี่โมง', 'What / What time', 'what time do you|what time is|what do you do'],
          [17, 'คุณซื้อผักที่ไหน / คุณ…เมื่อไร', 'Where / When', 'where do you|when do you|when did you'],
          [18, 'ทำไมคุณ… / ทำไมคุณไม่…', "Why / Because / Why don't you …?", "why do you|why don't you|because i"],
          [19, 'คุณไปทำงานอย่างไร / บ่อยแค่ไหน', 'How / How often', 'how do you|how often|by bus|by car']
        ]},
        { name: 'หมวด 3 อยาก มี ชอบ', lessons: [
          [20, 'ฉันอยากได้เค้ก / ฉันต้องการช้อน', 'want / need + สิ่งของ', 'i want a|i need a|i need some|you need'],
          [21, 'ฉันอยากเจอคุณ', 'want to / need to + กริยา', 'i want to|i need to|want to see|need to talk'],
          [22, 'ฉันชอบทำอาหารมาก / งานอดิเรกของฉันคืออ่านหนังสือ', 'like / love / enjoy + -ing', 'i love cooking|i like playing|i enjoy|my hobby'],
          [23, 'ฉันขอสั่งข้าวผัด', "I'd like … / Would you like …?", "i'd like|would you like|i would like"],
          [24, 'มีชาเย็นไหม', 'Do you have …?', 'do you have any|do you have a|have you got'],
          [25, 'คุณชอบเพลงแนวไหน', 'What kind of …? / Which …, A or B?', 'what kind of|which one|which is']
        ]},
        { name: 'หมวด 4 ทำได้ ต้องทำ ขอร้อง ชวน', lessons: [
          [26, 'ฉันทำอาหารได้ / ฉันกินปลาไม่ได้', "can / can't", "i can cook|i can't|you can|we can't"],
          [27, 'ฉันเก่งคณิตศาสตร์', 'be good at', "good at|i'm good at|not good at"],
          [28, 'ฉันต้องตื่นตี 5', 'have to / has to', 'i have to|she has to|you have to|we have to'],
          [29, 'คุณควรพักผ่อน', "should / shouldn't", "you should|you shouldn't|we should|i should"],
          [30, 'กรุณารอสักครู่ / อย่าจับนะ', "Please … / Don't …", "please wait|don't touch|please don't|don't worry"],
          [31, 'ไปกินข้าวนอกบ้านกัน', "Let's …", "let's go|let's eat|let's do|let's get"],
          [32, 'ขอยืมปากกาหน่อยได้ไหม / ช่วยฉันหน่อยได้ไหม', 'Can I …? / Can you …?', 'can i borrow|can you help|can i have|can you']
        ]},
        { name: 'หมวด 5 ตอนนี้กำลังทำ', lessons: [
          [33, 'ฉันกำลังทำงาน', 'am / is / are + -ing', "i'm working|she's cooking|we're going|i'm doing"],
          [34, 'คุณกำลังทำอะไรอยู่', 'ปฏิเสธและคำถาม -ing', "what are you doing|are you going|i'm not going|is it working"]
        ]},
        { name: 'หมวด 6 ถามเรื่องต่าง ๆ และเชื่อมประโยค', lessons: [
          [35, 'นี่คืออะไร / เขาคือใคร', 'What / Who / Whose / Which', "what is this|who is that|whose is|which one"],
          [36, 'ราคาเท่าไร / มีกี่คน', 'How much / How many', 'how much is|how much does|how many people|how many'],
          [37, 'ไปสนามบินใช้เวลานานแค่ไหน', 'How long does it take? / How far', 'how long does it take|how far|how long will'],
          [38, 'ทำไมร้านปิด', "Why + is / are / can't", "why is|why are|why can't"],
          [39, 'ฉันไม่มีรถ ก็เลยนั่งรถเมล์ไปทำงาน', 'and / but / so', 'so i|but i|and then']
        ]}
      ]},
      { name: 'เล่ม 2', sections: [
        { name: 'หมวด 1 เมื่อวานเกิดอะไรขึ้น', lessons: [
          [1, 'เมื่อคืนฉันเหนื่อย', 'was / were + คำคุณศัพท์', 'i was tired|it was great|we were|was so'],
          [2, 'แม่ของฉันเคยเป็นครู', 'was / were + คำนาม / สถานที่ / There was / were', 'was a teacher|there was a|there were|she was a'],
          [3, 'เมื่อวานฉันเล่นเกม', 'กริยาช่องที่ 2', 'yesterday i|last night i|i played|i went'],
          [4, 'ฉันไม่ได้ไปทำงาน', "didn't + ช่องที่ 1", "i didn't go|didn't have|i didn't know|didn't want"],
          [5, 'คุณเจอเธอไหม', 'Did …?', 'did you see|did you go|did you have|did she'],
          [6, 'เมื่อเช้าคุณตื่นนอนกี่โมง', 'What / What time did …? / What happened?', 'what happened|what time did|what did you'],
          [7, 'คุณไปไหนมา / คุณซื้อมาเมื่อไร', 'Where / When did …?', 'where did you|when did you|where have you been'],
          [8, 'ทำไมคุณร้องไห้ / ทำไมคุณไม่โทรหาฉัน', "Why did …? / Why didn't …?", "why did you|why didn't you"],
          [9, 'คุณรู้ได้อย่างไร / คุณไปกับใคร', 'How did …? / Who did … with?', 'how did you|who did you|how did it'],
          [10, 'ฉันเกิดปี 1990', 'was / were born', 'was born|were born|i was born'],
          [11, 'ฉันซื้อมันเมื่อ 2 วันที่แล้ว', '… ago', 'years ago|days ago|a long time ago|weeks ago'],
          [12, 'ฉันกำลังนอนอยู่ตอนที่คุณโทรมา', 'was / were + -ing + when', 'i was sleeping|was walking|when i was|were talking']
        ]},
        { name: 'หมวด 2 อนาคต', lessons: [
          [13, 'ฉันจะถือกระเป๋าให้คุณ', "will / won't", "i'll|i will|i won't|it will be"],
          [14, 'คุณจะรอฉันไหม', 'Will …? / Shall I …?', 'will you|shall i|shall we'],
          [15, 'ฉันจะไปเยี่ยมแม่', 'be going to', "i'm going to|we're going to|going to visit|gonna"],
          [16, 'ฉันกำลังจะนอนแล้ว', 'be about to', "about to|i'm about to|was about to"],
          [17, 'ฉันกำลังคิดจะ… / ฉันวางแผนจะ…', 'thinking of + -ing / plan to', 'thinking of|thinking about|plan to|planning to'],
          [18, 'ฉันยินดีจ่ายเพิ่ม', "be willing to / won't (ไม่ยอม)", "willing to|won't let|won't do"],
          [19, 'ถึงแล้วฉันจะโทรหาคุณ', 'will … when / after / before', "i'll call you|when i get|i'll let you know|before you"]
        ]},
        { name: 'หมวด 3 ประสบการณ์และสิ่งที่ทำมาถึงตอนนี้', lessons: [
          [20, 'ฉันล้างจานเสร็จแล้ว', 'have / has + ช่องที่ 3 / just / already', "i've just|i've already|have finished|has already"],
          [21, 'คุณเคยกินทุเรียนไหม', 'Have you (ever) …?', 'have you ever|have you been|have you seen'],
          [22, 'คุณยังทำไม่เสร็จเหรอ', "haven't … yet", "haven't|not yet|yet|hasn't"],
          [23, 'คุณเคยไปที่นั่นกี่ครั้ง', 'How many times …? / been to / gone to', 'how many times|been to|gone to'],
          [24, 'คุณอาศัยอยู่ที่นี่มานานแค่ไหนแล้ว', 'How long have …? / for / since', 'how long have|for years|since i|ever since'],
          [25, 'ฉันรอมาชั่วโมงหนึ่งแล้ว', 'have been + -ing', "i've been|have been waiting|been working|been doing"]
        ]},
        { name: 'หมวด 4 ขอร้องและขออนุญาตอย่างสุภาพ', lessons: [
          [26, 'ขออนุญาต…ได้ไหมคะ', 'May I …? / Can I please …?', 'may i|can i please|could i'],
          [27, 'รบกวนช่วย…หน่อยได้ไหมคะ', 'Could you please …?', 'could you please|could you|would you please'],
          [28, 'คุณจะว่าอะไรไหมถ้าฉัน…', 'Do you mind if I …? / Would you mind + -ing?', 'do you mind|would you mind|mind if i'],
          [29, 'ถ้า…จะโอเคไหม / เป็นไปได้ไหมที่จะ…', 'Is it OK if …? / Is it possible to …?', 'is it okay if|is it possible|is that okay'],
          [30, 'ฉันอยากให้คุณทำความสะอาดห้อง', 'want / ask / tell + คน + to', 'want you to|asked me to|told me to|tell him to'],
          [31, 'ช่วยหยุดคุยได้ไหม', 'stop / keep + -ing', 'stop talking|keep going|stop it|keep trying'],
          [32, 'กรุณาอย่า… / ไม่อนุญาตให้…', "Please don't … / not allowed to", "please don't|not allowed|you can't"],
          [33, 'ขอโทษนะ ฉันคง…ไม่ได้', "I'm afraid …", "i'm afraid|afraid not|i'm sorry but"],
          [34, 'จะขอบคุณมากถ้าคุณ…', "I'd appreciate it if you could …", "appreciate it|i'd appreciate|really appreciate"],
          [35, 'ตามสบายเลยนะ', 'Please feel free to … / Help yourself.', 'feel free|help yourself|go ahead'],
          [36, 'ไม่จำเป็นต้อง…', "There's no need to …", "no need to|don't need to|you don't have to"]
        ]}
      ]},
      { name: 'เล่ม 3', sections: [
        { name: 'หมวด 1 ชวน แนะนำ เตือน', lessons: [
          [1, '…ดีไหม', 'How about + -ing / คำนาม?', 'how about|what about'],
          [2, 'ให้ฉัน…เองนะ', 'Let me … / Let me know …', 'let me|let me know|let me see'],
          [3, 'ควรค่าแก่การลอง', 'be worth + -ing / worth it', 'worth it|worth trying|worth watching|worth the'],
          [4, 'อย่าลืม…นะ', "Don't forget to … / Remember to … / forgot to …", "don't forget|remember to|forgot to"],
          [5, 'ฉันแนะนำให้…', 'I suggest (that) you … / I recommend …', 'i suggest|recommend|i would recommend|suggest']
        ]},
        { name: 'หมวด 2 ความชอบและความรู้สึก', lessons: [
          [6, 'ฉันสนใจ…', 'be interested in + คำนาม / -ing', 'interested in|really interested'],
          [7, 'ช่วงนี้ฉันติด…', 'be into + คำนาม / -ing', "i'm into|really into|i'm really into"],
          [8, 'ฉันอยาก… (ตอนนี้)', 'feel like + -ing / คำนาม', "feel like|don't feel like|i feel like"],
          [9, 'ฉันเบื่อ…แล้ว', 'be tired of / be sick of', 'tired of|sick of|fed up'],
          [10, 'ฉันชอบ…มากกว่า…', 'prefer A to B / would rather … than …', 'i prefer|would rather|rather than'],
          [11, 'ฟังดู…นะ', 'That sounds + คำคุณศัพท์ / sounds like …', 'sounds good|sounds like|that sounds'],
          [12, 'ดูเหมือน…', 'look + คำคุณศัพท์ / look like / It looks like …', 'looks like|you look|it looks'],
          [13, 'มันทำให้ฉัน…', 'make + คน + คำคุณศัพท์ / ช่องที่ 1', 'makes me|made me|make you feel']
        ]},
        { name: 'หมวด 3 ความคิดเห็นและความสงสัย', lessons: [
          [14, 'คุณรู้สึกอย่างไรกับ…', 'How do you feel about …? / What do you think of …?', 'how do you feel|what do you think|think about'],
          [15, '…เป็นอย่างไรบ้าง', 'What is … like?', "what's it like|what is it like|what was it like"],
          [16, 'ขึ้นอยู่กับ…', 'It depends on …', 'it depends|depends on|depending on'],
          [17, 'ฉันสงสัยว่า…', 'I wonder if … / I was wondering if you could …', 'i wonder|i was wondering|wondering if'],
          [18, 'ฉันหวังว่า…', 'I hope + ประโยค / I hope to …', 'i hope|hope you|hopefully']
        ]},
        { name: 'หมวด 4 เวลา เงิน ความพยายาม', lessons: [
          [19, 'ต้องใช้…ในการ…', 'It takes / took + (คน) + เวลา + to …', 'it takes|it took|took me'],
          [20, 'ถึงเวลา…แล้ว', "It's time for … / It's time to …", "it's time|time to go|time for"],
          [21, 'ฉันกำลังพยายาม… / ฉันพยายามไม่…', 'trying to … / try not to …', 'trying to|try not to|tried to'],
          [22, 'ฉันใช้เงินไปกับ…', 'spend + เงิน + on … / spend + เวลา + -ing', 'spend|spent|spending time'],
          [23, 'ฉันจ่าย…ทุกเดือน', 'pay + ค่าใช้จ่าย / pay … for … / pay by / in …', 'pay for|paid for|pay the'],
          [24, 'ฉันอยากพัฒนา…', 'want to improve … / get better at …', 'improve|get better|better at']
        ]},
        { name: 'หมวด 5 สมมุติและความเป็นไปได้', lessons: [
          [25, 'ถ้าฉันเป็นคุณ ฉันจะ…', "If I were you, I'd … / If + ช่องที่ 2, … would …", "if i were you|if i were|i would|if i had"],
          [26, 'ถ้า…ล่ะ จะทำยังไง', 'What if …?', 'what if'],
          [27, 'จะเป็นไปได้ไหมที่จะ…', 'Would it be possible to …?', 'would it be possible|is it possible|possible to'],
          [28, 'มีวิธี…ไหม', 'Is there a way to …? / The best way to … is …', 'a way to|the best way|is there a way'],
          [29, 'มีโอกาสไหมที่…', 'Is there any chance …?', 'any chance|a chance|chances are']
        ]},
        { name: 'หมวด 6 ระดับและความสามารถ', lessons: [
          [30, '…เกินกว่าจะ…', 'too + คำคุณศัพท์ + to … / too much / too many', 'too much|too many|too late|too hard'],
          [31, '…พอที่จะ…', 'คำคุณศัพท์ + enough to … / enough + คำนาม', 'enough to|enough time|big enough|good enough'],
          [32, 'ฉันสามารถ…ได้', 'be able to / was able to / will be able to', 'able to|was able to|be able to'],
          [33, 'นี่เป็นครั้งแรกที่ฉัน…', "It's the first time I've + ช่องที่ 3 / my first time + -ing", 'the first time|first time i|my first time']
        ]},
        { name: 'หมวด 7 ประหลาดใจ ยืนยัน ขอความช่วยเหลือ', lessons: [
          [34, 'มิน่าล่ะ…', 'No wonder + ประโยค', 'no wonder'],
          [35, 'ฉันเพิ่งรู้ว่า…', 'I just found out … / find out about …', 'found out|find out|just found out'],
          [36, 'คุณไม่…เหรอ', "Don't / Doesn't / Isn't / Didn't …?", "don't you|didn't you|isn't it|doesn't it"],
          [37, 'ฉันทำยังไงก็…ไม่ได้สักที', "can't seem to … / seem to …", "can't seem|seems to|seem to"],
          [38, 'ช่วย…หน่อยได้ไหม', 'Can you give me a hand with …?', 'give me a hand|give you a hand|help me with|can you help'],
          [39, 'คุณจะสะดวก…ไหม', 'Would you be available …?', 'available|are you free'],
          [40, 'รับ…ไหม', 'Would you care for …? / Would you care to …?', 'care for|would you care|would you like']
        ]}
      ]}
    ]
  },
  grammar: {
    name: 'ไวยากรณ์ A1–A2',
    volumes: [
      { name: 'A1', sections: [
        { name: 'A1 เล่ม 1 (บท 1–14)', lessons: [
          [1, 'Subject Pronouns', 'I / you / he / she / it / we / they', 'we are|they are|she is'],
          [2, 'Verb to Be: Affirmative', 'am / is / are', "i'm a|she's a|we're"],
          [3, 'Verb to Be: Negative', "I'm not / isn't / aren't", "i'm not|it isn't|they aren't"],
          [4, 'Verb to Be: Yes/No Questions', 'Am / Is / Are …?', 'are you|is it|yes i am'],
          [5, 'Verb to Be: Wh-Questions 1', 'What / Where / Who / How old', "what's your name|where are you from|how old"],
          [6, 'A and An', 'a / an', "it's a|he's an|an apple"],
          [7, 'The', 'the', 'the door|the end|the first'],
          [8, 'Adjective Position', 'adjective + noun / be + adjective', "a big|it's beautiful|a little"],
          [9, 'Plural Nouns 1', '-s / -es / -ies', 'two books|boxes|cities'],
          [10, 'Plural Nouns 2', 'พหูพจน์ไม่ปกติ', 'children|people|women'],
          [11, 'This, That, These and Those', 'this / that / these / those', "what's this|those are|these are"],
          [12, 'Possessive Adjectives', 'my / your / his / her / its / our / their', 'my name is|her brother|their house'],
          [13, "Possessive 's", "noun + 's", "mother's|father's|friend's"],
          [14, 'Whose…?', 'Whose + noun …?', 'whose']
        ]},
        { name: 'A1 เล่ม 2 (บท 15–28)', lessons: [
          [15, 'Countable and Uncountable Nouns', 'a / an / some', 'some water|an apple|some money'],
          [16, 'There Is and There Are', 'There is / There are', "there's a|there are"],
          [17, "There Isn't and There Aren't", "There isn't / There aren't", "there isn't|there aren't|there's no"],
          [18, 'Is There? and Are There?', 'Is there …? / Are there …?', 'is there a|are there any'],
          [19, 'Some and Any', 'some / any', 'some more|any questions|anything'],
          [20, 'Much, Many, A Lot of, Lots of + How much / How many', 'much / many / a lot of', 'how much is|how many|a lot of'],
          [21, 'A Few and A Little', 'a few / a little', 'a few|a little bit'],
          [22, 'Prepositions of Place 1', 'in / on / at', 'in the box|on the table|at home'],
          [23, 'Prepositions of Place 2', 'under / behind / between / next to / in front of', 'behind the|in front of|next to|between'],
          [24, 'Prepositions of Time', 'at / on / in', 'on monday|in may|at night'],
          [25, 'Object Pronouns', 'me / you / him / her / it / us / them', 'call me|tell him|help us'],
          [26, 'Spelling Rules -s / -es / -ing / -ed', 'การเติมท้ายคำ', 'watches|studying|stopped'],
          [27, 'Present Simple: I, You, We and They', 'subject + V1', 'i usually|we live in|i work'],
          [28, 'Present Simple: He, She and It', 'subject + V-s', 'she works|he lives|it takes']
        ]},
        { name: 'A1 เล่ม 3 (บท 29–42)', lessons: [
          [29, 'Present Simple: Negative', "don't / doesn't + V1", "i don't|she doesn't"],
          [30, 'Present Simple: Yes/No Questions', 'Do / Does …?', 'do you like|does she'],
          [31, 'Present Simple: Wh-Questions + What time / What kind of / What colour / Which', 'Wh- + do / does …?', 'what time do you|what kind of|which one'],
          [32, 'Subject Questions', 'Who / What + verb', 'who wants|what happened'],
          [33, 'Have and Has: Affirmative', 'have / has', 'i have a|she has|have breakfast'],
          [34, 'Have and Has: Negative', "don't have / doesn't have", "i don't have|doesn't have"],
          [35, 'Do you have…?', 'Do you have …?', 'do you have any|do you have a'],
          [36, 'Have Got and Has Got', 'have got / has got', "i've got|she's got"],
          [37, 'Adverbs of Frequency', 'always / usually / often / sometimes / never', 'i always|usually|never|once a week'],
          [38, 'and / but / or / because', 'conjunctions', 'because i|but i think'],
          [39, 'How Often / How Long / How Far', 'How often / How long / How far', 'how often|how long does|how far'],
          [40, 'Verb to Be: Wh-Questions 2', 'When / Why / How / How tall / How big', 'why are you|how are you|how tall'],
          [41, 'Wh-Questions Review', 'is / are หรือ do / does', 'where do you|where are you'],
          [42, 'Can: Ability', "can / can't", "i can|i can't|can you swim"]
        ]},
        { name: 'A1 เล่ม 4 (บท 43–56)', lessons: [
          [43, 'Can: Permission and Requests', 'Can I …? / Can you …?', 'can i|can you help'],
          [44, "Imperatives and Let's", "V1 … / Don't … / Let's …", "stand up|sit down|let's go|kneel down|breathe in"],
          [45, 'Like, Love and Hate + -ing', 'like / love / hate + V-ing', 'i love being|i love doing|i like being|i hate being|love watching|like playing|love working'],
          [46, 'Want and Need + To Infinitive', 'want / need + to + V1', 'i want to|i need to'],
          [47, 'Would Like', "I'd like … / Would you like …?", "i'd like|would you like"],
          [48, 'Present Continuous: Affirmative', 'am / is / are + V-ing', "i'm cooking|she's running|we're going"],
          [49, 'Present Continuous: Negative', "am not / isn't / aren't + V-ing", "i'm not going|it isn't working"],
          [50, 'Present Continuous: Yes/No Questions', 'Am / Is / Are … V-ing?', 'are you okay|is it raining|are you going'],
          [51, 'Present Continuous: Wh-Questions', 'Wh- + am / is / are … V-ing?', 'what are you doing|where are you going'],
          [52, 'Present Simple or Present Continuous', 'นิสัย / กำลังทำ', 'usually|right now|at the moment'],
          [53, 'Adverbs of Manner', 'adjective + -ly', 'slowly|carefully|quickly'],
          [54, 'Adverbs of Degree', 'very / really / too', 'really good|very tired|too hot'],
          [55, 'Comparative Adjectives 1', 'คำสั้น + -er + than', 'bigger than|older than'],
          [56, 'Comparative Adjectives 2', 'more + คำยาว / irregular', 'more expensive|better than']
        ]},
        { name: 'A1 เล่ม 5 (บท 57–70)', lessons: [
          [57, 'Superlative Adjectives 1', 'the + คำสั้น + -est', 'the biggest|the best'],
          [58, 'Superlative Adjectives 2', 'the most + คำยาว / irregular', 'the most important|the worst'],
          [59, 'Was and Were: Affirmative', 'was / were', 'i was|it was great'],
          [60, 'Was and Were: Negative', "wasn't / weren't", "wasn't|weren't"],
          [61, 'Was and Were: Questions', 'Was / Were …?', 'how was your|were you'],
          [62, 'Past Simple: Regular Verbs', 'V-ed', 'i worked|we watched|she played'],
          [63, 'Past Simple: Irregular Verbs', 'V2', 'i went|i saw|we had'],
          [64, 'Past Simple: Negative', "didn't + V1", "i didn't know|didn't go"],
          [65, 'Past Simple: Yes/No Questions', 'Did …?', 'did you see|did you have'],
          [66, 'Past Simple: Wh-Questions', 'Wh- + did …?', 'what did you|where did you go'],
          [67, 'Will for the Future: บอกเล่า', 'will + V1', "i'll|it will be"],
          [68, 'Will: ปฏิเสธและคำถาม', "won't / Will …?", "will you|i won't"],
          [69, 'Be Going To: บอกเล่าและปฏิเสธ', 'am / is / are + going to', "i'm going to|we're not going to"],
          [70, 'Be Going To: คำถาม', 'Are you going to …?', 'are you going to|what are you going to']
        ]}
      ]},
      { name: 'A2', sections: [
        { name: 'A2 เล่ม 1 (บท 1–14)', lessons: [
          [1, 'Possessive Pronouns', 'mine / yours / his / hers / ours / theirs', "it's mine|is this yours|hers"],
          [2, 'Reflexive Pronouns', 'myself / yourself …', 'by myself|help yourself|yourself'],
          [3, 'Indefinite Pronouns 1', 'some- / any-', 'something|anyone|somewhere'],
          [4, 'Indefinite Pronouns 2', 'every- / no-', 'everyone|nothing|nobody'],
          [5, 'One and Ones', 'the … one / ones', 'the red one|which one|the other one'],
          [6, 'The and Zero Article', 'the / –', 'go to school|the cinema|go to bed'],
          [7, 'Few / A Few and Little / A Little', 'few / a few / little / a little', 'very few|a little time|very little'],
          [8, 'All, Most, Some and None', 'all / most / some / none of', 'most of them|none of|all of us'],
          [9, 'Every and Each', 'every / each', 'every day|each of'],
          [10, 'Partitives and Containers', 'a cup of / a piece of / a bottle of', 'a cup of|a piece of|a bottle of'],
          [11, 'There Was and There Were', 'There was / There were', 'there was a|there were no'],
          [12, 'Was there? / Were there?', 'Was there …? / Were there …?', 'was there any|were there'],
          [13, 'Prepositions of Movement 1', 'to / into / out of / from', 'go into|get out of|come from'],
          [14, 'Prepositions of Movement 2', 'up / down / across / through / along / past', 'go through|walk along|across the|past the']
        ]},
        { name: 'A2 เล่ม 2 (บท 15–28)', lessons: [
          [15, 'คำบอกช่วงเวลา', 'for / during / from…to / by / until', 'for two hours|until|by friday'],
          [16, 'Prepositions after Verbs', 'listen to / wait for / look at', 'listen to|wait for|look at'],
          [17, 'Prepositions by / with / about', 'go by bus / cut with a knife / talk about', 'by bus|cut it with|talk about'],
          [18, 'Comparative Adverbs', 'faster / more carefully', 'faster than|more carefully'],
          [19, 'Comparative Modifiers', 'much / a bit / far + comparative', 'much better|a bit more|far bigger'],
          [20, 'As…As and Not As…As', 'as … as / not as … as', 'as soon as|not as good as'],
          [21, 'Adjectives Ending in -ed and -ing', 'bored / boring', "i'm bored|it's boring|excited"],
          [22, 'Adjective + Preposition', 'afraid of / good at / interested in', 'afraid of|good at|interested in'],
          [23, 'Adjective Order', 'opinion + size + age + …', 'a nice little|a big old|beautiful little|lovely little|nice big|great big'],
          [24, 'Too', 'too + adjective / too much / too many', 'too expensive|too much|too many'],
          [25, 'Enough', 'enough + noun / adjective + enough', 'enough time|big enough'],
          [26, 'Adjective + To Infinitive', 'adjective + to + V1', 'nice to meet you|easy to|happy to'],
          [27, 'Could: Past Ability', "could / couldn't", "i couldn't|could you"],
          [28, 'Could and May: Polite Requests', 'Could you …? / May I …?', 'could you please|may i']
        ]},
        { name: 'A2 เล่ม 3 (บท 29–42)', lessons: [
          [29, 'Offers', 'Shall I …? / Would you like me to …?', 'shall i|would you like me to'],
          [30, 'Suggestions', "Why don't we …? / How about …? / What about …?", "why don't we|how about|what about"],
          [31, 'Should and Ought To', 'should / ought to', 'you should|ought to'],
          [32, "Have To and Don't Have To", "have to / don't have to", "i have to|you don't have to"],
          [33, "Need, Needn't and Don't Need To", "need to / needn't / don't need to", "you don't need to|i need"],
          [34, "Had To and Didn't Have To", "had to / didn't have to", "i had to|didn't have to"],
          [35, "Must and Mustn't", "must / mustn't", "you must|mustn't"],
          [36, 'Must or Have To', 'must / have to', 'must|have to'],
          [37, 'May and Might', 'may / might', 'it might|i may be|might be'],
          [38, 'Modal Verbs Review', 'can / could / should / must / have to / might', 'should|could|might'],
          [39, 'Verbs with Two Objects', 'give / send / show + person + thing', 'give me|send her|show you'],
          [40, 'Phrasal Verbs 1 (แยกกรรมได้)', 'turn it off / pick it up', 'turn it off|pick it up|put on|take off'],
          [41, 'Phrasal Verbs 2 (แยกกรรมไม่ได้)', 'get up / look after', 'get up|lie down|look after|roll over'],
          [42, 'Past Continuous: Affirmative', 'was / were + V-ing', 'i was walking|they were']
        ]},
        { name: 'A2 เล่ม 4 (บท 43–56)', lessons: [
          [43, 'Past Continuous: Negative', "wasn't / weren't + V-ing", "i wasn't listening|weren't"],
          [44, 'Past Continuous: Questions', 'Was / Were … V-ing?', 'what were you doing|were you'],
          [45, 'Past Simple or Past Continuous', 'when / while', 'when i was|while i was'],
          [46, 'Time Clauses', 'before / after / when + ประโยค', 'before i|after we|when he'],
          [47, 'Used To', 'used to + V1', "i used to|didn't use to"],
          [48, 'Past Forms Review', 'Past Simple / Past Continuous / Used To', 'used to|was doing|did'],
          [49, 'Past Participles (V3)', 'V3', 'taken|eaten|written'],
          [50, 'Present Perfect: Affirmative', 'have / has + V3', "i've been|she has done"],
          [51, 'Present Perfect: Negative', "haven't / hasn't + V3", "i haven't|she hasn't"],
          [52, 'Present Perfect: Questions', 'Have / Has … V3?', 'have you ever|has anyone'],
          [53, 'Ever and Never', 'ever / never', "have you ever|i've never"],
          [54, 'Just, Already and Yet', 'just / already / yet', "i've just|already|not yet"],
          [55, 'Present Perfect: For and Since', 'for / since', 'for years|since'],
          [56, 'Present Perfect or Past Simple', 'have done / did', 'have you been|when did you go']
        ]},
        { name: 'A2 เล่ม 5 (บท 57–70)', lessons: [
          [57, 'Present Continuous for Future Plans', 'am / is / are + V-ing (อนาคต)', "i'm meeting|we're leaving tomorrow"],
          [58, 'Will or Be Going To 1: แผน / ตัดสินใจตอนพูด', 'will / be going to', "i'll get it|i'm going to"],
          [59, 'Will or Be Going To 2: การคาดการณ์', 'will / be going to', "going to rain|it's going to be|i think it will|it will be"],
          [60, 'Verb + To Infinitive', 'decide / hope / try + to', 'i decided to|i hope to|try to'],
          [61, 'Verb + -ing', 'enjoy / stop / prefer + V-ing', 'i enjoy|stop talking|i prefer'],
          [62, 'Infinitive of Purpose', 'to / for', 'i went there to|in order to'],
          [63, 'Relative Clauses 1', 'who / which / that', 'the man who|something that|which is'],
          [64, 'Relative Clauses 2', 'ละ who / which / that', 'the people we|the thing i'],
          [65, 'Preposition Questions', 'Who are you talking to?', 'talking to|looking for|what are you talking about|who are you'],
          [66, 'Questions with Like', 'What is it like? / What does he look like?', "what's it like|what does he look like"],
          [67, 'Connectors 1: เหตุผล', "so / because / that's why", "that's why|because of"],
          [68, 'Connectors 2: ขัดแย้ง', 'but / although / however', 'although|however'],
          [69, 'Zero Conditional', 'If + present, present', 'if you heat|when you'],
          [70, 'First Conditional', "If + present, will", "if you want|if it rains|i'll"]
        ]}
      ]}
    ]
  }
};
