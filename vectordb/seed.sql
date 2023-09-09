INSERT INTO collection (parent_collection_id, name, description, image_url)
VALUES
    (NULL, 'Social Media', 'Social media companies', 'https://example.com/collection1.jpg'),
    (1, 'Twitter', 'x.com', 'https://example.com/collection2.jpg'),
    (1, 'Facebook', 'meta and stuff', 'https://example.com/collection3.jpg');

INSERT INTO class (name, description, image_url)
VALUES
    ('Terms of Service', 'Terms of Service documents', 'https://example.com/class1.jpg'),
    ('Privacy Policy', 'Privacy Policy documents', 'https://example.com/class2.jpg'),
    ('Other', 'Other documents', 'https://example.com/class3.jpg');

INSERT INTO file (url, title, description, class_id, collection_id)
VALUES
    ('https://twitter.com/en/tos#:~:text=Your%20use%20of%20the%20Services%20is%20at%20your%20own%20risk,content%20posted%20by%20other%20users.', 'X Terms of Service', 'foobar', 1, 2),
    ('https://twitter.com/en/privacy', 'X Privacy Policy', 'foobar', 2, 2),
    ('https://m.facebook.com/legal/terms', 'Facebook Terms of Service', 'foobar', 1, 3);
    ('https://www.facebook.com/privacy/policy/', 'Facebook Privacy Policy', 'foobar', 2, 3)
