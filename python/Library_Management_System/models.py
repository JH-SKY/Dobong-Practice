# 0. [Config] 시스템 설정 관리 클래스
class LibraryConfig:
    LOAN_LIMIT = 3  # 통합 대출 한도 (실무에선 여기서 한 번에 관리함)

# 1. [Book] 도서 정보 및 상태 관리
class Book:
    def __init__(self, title, author, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
        self.is_deleted = False

    def borrow(self):
        self.is_available = False

    def return_book(self):
        self.is_available = True
        
    def mark_as_deleted(self):
        """[2번 반영] 소프트 딜리트 처리"""
        self.is_deleted = True
        self.is_available = False

# 2. [User] 공통 부모 클래스
class User:
    def __init__(self, name):
        self.name = name

# 3. [Member] 회원 클래스
class Member(User):
    def __init__(self, name, member_id):
        super().__init__(name)
        self.member_id = member_id
        self.borrowed_books = []

    def _add_book(self, book: Book):
        """[1번 반영] 내부용 메서드 (Library 클래스를 통해서만 호출 권장)"""
        self.borrowed_books.append(book)

    def _remove_book(self, book: Book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

# 4. [Librarian] 사서 클래스
class Librarian(User):
    def __init__(self, name, employee_id):
        super().__init__(name)
        self.employee_id = employee_id

    def register_book(self, library, book: Book):
        library.add_book(book)

# 5. [Library] 도서관 시스템 클래스 (통합 관리자)
class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)

    def remove_book(self, book: Book):
        """[2번 반영] 실제 삭제 대신 삭제 표시(Soft Delete)만 함"""
        if book in self.books:
            book.mark_as_deleted()
            print(f"시스템 알림: '{book.title}' 도서가 폐기 처리되었습니다. (데이터는 보존됨)")

    def process_loan(self, member, book: Book):
        # 1. 도서 유효성 체크
        if book.is_deleted or not book.is_available:
            print(f"대출 실패: '{book.title}'은(는) 현재 대출이 불가능하거나 폐기된 도서입니다.")
            return
        
        # 2. [3번 반영] 통합 대출 한도 체크 (Config 클래스 사용)
        if len(member.borrowed_books) >= LibraryConfig.LOAN_LIMIT:
            print(f"대출 거부: {member.name}님은 통합 한도({LibraryConfig.LOAN_LIMIT}권)를 초과했습니다.")
            return
        
        # 3. 대출 실행 (통제된 로직)
        book.borrow()           
        member._add_book(book)    
        print(f"대출 완료: {member.name}님이 {self.name}에서 '{book.title}'을(를) 빌렸습니다.")

    def process_return(self, member, book: Book):
        if book not in self.books:
            print(f"반납 오류: '{book.title}'은(는) {self.name}의 도서가 아닙니다.")
            return
        
        if book in member.borrowed_books:
            book.return_book()
            member._remove_book(book) 
            print(f"반납 완료: {member.name}님이 '{book.title}'을(를) 반납했습니다.")