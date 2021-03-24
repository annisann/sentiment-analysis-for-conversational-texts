# Sentiment Analysis for Conversational Texts

## parsing
1. cuma bisa gabungin 2 bubble chat terakhir. kalo ada 4, jadinya 3 bubble chat.
    - suggestions: looping ngecek ampe bener2 sama semua.
2. langsung di | daripada pake exceed space, karena ada bbrp bubble chat yang hilang.

## preprocessing
1. output tokennya bakal kosong karena banyak hal yang diremove pas cleaning.
    - solution: link gak diapus tapi diganti jadi <link>, etc
# LOG
- upload parsed_doc fix, double checked udah bener semua. karna sebelumnya masih ada '... omitted' (diganti jadi <DOC>) dan miss lainnya.
