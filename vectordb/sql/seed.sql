-- INSERT INTO user (username, hashed_password, salt, first_name, last_name, image_url)
-- VALUES
--     ('test', 'test', 'test', 'test', 'test', 'https://example.com/test.jpg'),
--     ('test2', 'test2', 'test2', 'test2', 'test2', 'https://example.com/test2.jpg');

-- INSERT INTO collection (user_id, parent_collection_id, name, description, image_url)
-- VALUES
--     (1, NULL, 'Default', 'Default collection', 'https://example.com/collection1.jpg'),
--     (1, NULL, 'Social Media', 'Social media companies', 'https://example.com/collection1.jpg'),
--     (1, 2, 'Twitter', 'x.com', 'https://example.com/collection2.jpg'),
--     (1, 2, 'Facebook', 'meta and stuff', 'https://example.com/collection3.jpg'),
--     (1, 1, 'OpenAI', 'OpenAI stuff', 'https://openai.com');

INSERT INTO file_class (name, description, image_url)
VALUES
    ('Terms of Service', 'Terms of Service documents', 'https://example.com/class1.jpg'),
    ('Privacy Policy', 'Privacy Policy documents', 'https://example.com/class2.jpg'),
    ('Other', 'Other documents', 'https://example.com/class3.jpg');

-- INSERT INTO file (url, name, description, file_class_id, collection_id)
-- VALUES
--     ('https://twitter.com/en/tos#:~:text=Your%20use%20of%20the%20Services%20is%20at%20your%20own%20risk,content%20posted%20by%20other%20users.', 'X Terms of Service', 'foobar', 1, 3),
--     ('https://twitter.com/en/privacy', 'X Privacy Policy', 'foobar', 2, 3),
--     ('https://m.facebook.com/legal/terms', 'Facebook Terms of Service', 'foobar', 1, 4),
--     ('https://www.facebook.com/privacy/policy/', 'Facebook Privacy Policy', 'foobar', 2, 4),
--     ('https://openai.com/policies/terms-of-use', 'OpenAI Terms of Use', 'foobar', 1, 5),
--     ('https://openai.com/policies/privacy-policy', 'OpenAI Privacy Policy', 'foobar', 2, 5);
