
content_form = 'wrk.method = \"POST\"\nwrk.body   = \"{\"Sender\":\"%s\",\"Data\":\"abc\"}\"\nwrk.headers[\"Content-Type\"] = \"application/x-www-form-urlencoded\"'

content_line_1 = 'wrk.method = "POST"'
content_line_3 = 'wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"'

for i in range(1):
    content_line_2 = 'wrk.body   = \"{\\\"Sender\\\":\\\"' + str(i) + '\\\",\\\"Data\\\":\\\"abc\\\"}\"'
    with open('./post_lua/post_{}.lua'.format(i), 'w') as f:
        f.write(content_line_1 + '\n')
        f.write(content_line_2 + '\n')
        f.write(content_line_3 + '\n')
        f.close()