from werkzeug.security import generate_password_hash
print(generate_password_hash('LaNuevaEs99.'))

32768:8:1$cF47X6Qlu7LvrTSt$92cca221938a76fa976dadf46e7aefc8795a50a5a5a249a097096767e653cf5e2fdf9477743efbde75e03cf2efcd8ba1a1cfdde7ee3433b63b1031963bb9b311 

UPDATE users
SET password = '32768:8:1$cF47X6Qlu7LvrTSt$92cca221938a76fa976dadf46e7aefc8795a50a5a5a249a097096767e653cf5e2fdf9477743efbde75e03cf2efcd8ba1a1cfdde7ee3433b63b1031963bb9b311'
WHERE email = 'pablo.martin.iglesiass@gmail.com';

SELECT * FROM users WHERE email = 'pablo.martin.iglesiass@gmail.com';

32768:8:1$08qqLi55xOtBIdiA$6125a8a9193cd4e5b21b2049fabe09341076e690d36349081920f12aef286886a43e41e870d34bfba5be481d4d98abddcf48b1d4c34b98cea6147a7d2707c3a2

INSERT INTO users (username, email, password, role)
VALUES ('admin_user', 'pablo.martin.iglesiass@gmail.com', '32768:8:1$08qqLi55xOtBIdiA$6125a8a9193cd4e5b21b2049fabe09341076e690d36349081920f12aef286886a43e41e870d34bfba5be481d4d98abddcf48b1d4c34b98cea6147a7d2707c3a2', 'admin');

pbkdf2:sha256:260000$T7ZtdRd2O4F9d3pr$6c3a7ab44d91535a3e1db2d2b9bb9f7fa4f6f62c21a26a3017a45e7f7bcde2b3

from werkzeug.security import generate_password_hash
print(generate_password_hash('LaNuevaEs99.'))

from werkzeug.security import generate_password_hash
print(generate_password_hash('LaNuevaEs99.', method='pbkdf2:sha256'))

pbkdf2:sha256:1000000$aabL6Yolga7nYdwl$6b0016b05cd998e2ed14157fe66441d97d3631e59d5c42a45cc2028e7458d5bf

UPDATE users
SET password = 'pbkdf2:sha256:1000000$aabL6Yolga7nYdwl$6b0016b05cd998e2ed14157fe66441d97d3631e59d5c42a45cc2028e7458d5bf'
WHERE role = 'admin';

INSERT INTO users (username, email, password, role)
VALUES ('admin_user', 'pablo.martin.iglesiass@gmail.com', 'pbkdf2:sha256:1000000$aabL6Yolga7nYdwl$6b0016b05cd998e2ed14157fe66441d97d3631e59d5c42a45cc2028e7458d5bf', 'admin');
