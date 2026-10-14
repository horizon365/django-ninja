django ninja docs page पर एक अजीब समस्या: दो अलग endpoints एक ही समय पर खुल जाते हैं
==========================================================

हाल ही में, एक community member ने एक समस्या report की: docs page पर, दो endpoints में से किसी पर भी click करने से दोनों एक ही समय पर खुल जाते हैं। अन्य APIs में ऐसा व्यवहार नहीं होता।

![django-ninja-docs-wrong](/img/docs-wrong.png)


मूल कारण अंततः पाया गया: function के नाम या paths duplicate थे। दूसरे शब्दों में, view लिखते समय एक function को copy किया गया और उसका नाम बदलना भूल गए।
