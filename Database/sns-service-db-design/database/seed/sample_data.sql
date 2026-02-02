-- 1. 사용자 (nickname, email 사용)
INSERT INTO users (nickname, email, password, bio) VALUES 
('chulsoo_gym', 'chul@test.com', 'pass123', '오운완! 운동하는 철수입니다.'), -- id 1
('younghee_art', 'young@test.com', 'pass456', '그림 그리는 영희의 일상'),     -- id 2
('minsu_study', 'min@test.com', 'pass789', '비전공자 개발자 도전기!');       -- id 3

-- 2. 팔로우 & 차단 (셀프 조인 구조)
INSERT INTO follows (follower_id, following_id) VALUES (2, 1), (3, 1); -- 영희와 민수가 철수를 팔로우
INSERT INTO blocks (blocker_id, blocked_id) VALUES (1, 3);            -- 철수가 민수를 차단

-- 3. 게시글 및 이미지
INSERT INTO posts (user_id, content, like_count) VALUES (1, '오늘 어깨 운동 완료! #오운완 #운동', 1); -- post id 1
INSERT INTO feedimage (post_id, image_url) VALUES (1, 'https://storage.com/photo1.jpg');

-- 4. 댓글 및 대댓글 (parent_comment_id 사용)
INSERT INTO comments (post_id, user_id, content) VALUES (1, 2, '대단해요!'); -- comment id 1 (영희의 댓글)
INSERT INTO comments (post_id, user_id, parent_comment_id, content) 
VALUES (1, 1, 1, '감사합니다 영희님!'); -- comment id 2 (철수의 답글/대댓글)

-- 5. 좋아요 및 북마크
INSERT INTO feedlike (post_id, user_id) VALUES (1, 2);
INSERT INTO feedbookmark (post_id, user_id) VALUES (1, 2);

-- 6. 해시태그 연결
INSERT INTO hashtag (name) VALUES ('오운완'), ('운동'); -- id 1, 2
INSERT INTO posthashtag (post_id, hashtag_id) VALUES (1, 1), (1, 2);

-- 7. 알림 (receiver_id 사용)
INSERT INTO notification (receiver_id, sender_id, type, target_id) 
VALUES (1, 2, 'COMMENT', 1); -- 영희가 철수에게 댓글 알림 보냄

-- 8. 채팅 (방 생성 -> 참여자 추가 -> 메시지)
INSERT INTO chatroom (room_name, is_group) VALUES ('철수와 영희의 대화', 0); -- chatroom id 1
INSERT INTO chatparticipant (chatroom_id, user_id) VALUES (1, 1), (1, 2);
INSERT INTO chatmessage (chatroom_id, user_id, content) VALUES (1, 2, '철수님 오늘 운동 가시나요?');