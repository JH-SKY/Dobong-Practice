-- [전체 통합본] ERD 이미지와 100% 일치시킨 설계

-- 1. 사용자 (users)
CREATE TABLE users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    email           VARCHAR(100) NOT NULL UNIQUE, -- 로그인 아이디
    password        VARCHAR(255) NOT NULL,        -- 비밀번호
    nickname        VARCHAR(50) NOT NULL UNIQUE,  -- ERD에 맞춰 username 대신 nickname 사용
    profile_image_url VARCHAR(255),
    bio             TEXT,
    is_private      TINYINT(1) DEFAULT 0,         -- 비공개 계정 여부
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      DATETIME NULL
);

-- 2. 팔로우 (follows)
CREATE TABLE follows (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    follower_id     INT NOT NULL,
    following_id    INT NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      DATETIME NULL,
    FOREIGN KEY (follower_id) REFERENCES users(id),
    FOREIGN KEY (following_id) REFERENCES users(id)
);

-- 3. 게시글 (posts)
CREATE TABLE posts (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    content         TEXT NOT NULL,
    like_count      INT DEFAULT 0,                -- ERD에 있는 좋아요 수 컬럼
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 4. 게시글 이미지 (feedimage)
CREATE TABLE feedimage (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    post_id         INT NOT NULL,
    image_url       VARCHAR(255) NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

-- 5. 댓글 (comments)
CREATE TABLE comments (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    post_id         INT NOT NULL,
    user_id         INT NOT NULL,
    parent_comment_id INT,                        -- [대댓글 기능] 셀프 조인용!
    content         VARCHAR(255) NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      DATETIME NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (parent_comment_id) REFERENCES comments(id)
);

-- 6. 좋아요 및 북마크 (feedlike, feedbookmark)
CREATE TABLE feedlike (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    post_id         INT NOT NULL,
    user_id         INT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE feedbookmark (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    post_id         INT NOT NULL,
    user_id         INT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 7. 해시태그 (hashtag, posthashtag)
CREATE TABLE hashtag (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE posthashtag (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    post_id         INT NOT NULL,
    hashtag_id      INT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (hashtag_id) REFERENCES hashtag(id)
);

-- 8. 알림 (notification)
CREATE TABLE notification (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    receiver_id     INT NOT NULL,                 -- ERD에 맞춰 user_id 대신 receiver_id
    sender_id       INT NOT NULL,
    type            VARCHAR(20) NOT NULL,
    target_id       INT,
    is_read         TINYINT(1) DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (receiver_id) REFERENCES users(id),
    FOREIGN KEY (sender_id) REFERENCES users(id)
);

-- 9. 차단 (blocks)
CREATE TABLE blocks (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    blocker_id      INT NOT NULL,                 -- 차단한 사람
    blocked_id      INT NOT NULL,                 -- 차단당한 사람
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      DATETIME NULL,
    FOREIGN KEY (blocker_id) REFERENCES users(id),
    FOREIGN KEY (blocked_id) REFERENCES users(id)
);

-- 10. 채팅 (chatroom, chatparticipant, chatmessage)
CREATE TABLE chatroom (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    room_name       VARCHAR(100),
    is_group        TINYINT(1) DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chatparticipant (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    chatroom_id     INT NOT NULL,
    user_id         INT NOT NULL,
    joined_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chatroom_id) REFERENCES chatroom(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE chatmessage (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    chatroom_id     INT NOT NULL,
    user_id         INT NOT NULL,
    content         TEXT NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chatroom_id) REFERENCES chatroom(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);