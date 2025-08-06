from generate_audio import generate
prompt_audio = open("prompt_audio.txt", "r").read()
content = """
Bí ẩn về cách deep learning hoạt động hả? Nghe có vẻ ghê gớm, nhưng thực ra nó cũng không đến nỗi phức tạp như người ta đồn đâu. Cứ coi như là mình đang dạy một đứa bé học vậy đó, nhưng mà là với một lượng dữ liệu khổng lồ và những phép tính toán học siêu tốc.
Nói đại khái là thế này: Deep learning, hay còn gọi là học sâu, nó là một nhánh của máy học. Cái "sâu" ở đây ám chỉ là nó có nhiều lớp "nơ-ron nhân tạo" xếp chồng lên nhau, giống như nhiều lớp củ hành tây vậy đó. Mỗi lớp này sẽ xử lý một phần thông tin, rồi chuyển kết quả qua cho lớp tiếp theo. Càng nhiều lớp, nó càng có khả năng học được những đặc điểm phức tạp hơn trong dữ liệu.
Thử hình dung nhé, nếu mình muốn máy nhận diện một con mèo trong ảnh đi. Lớp đầu tiên có thể chỉ nhận diện mấy cái đường nét cơ bản thôi, như cạnh hay góc. Rồi lớp tiếp theo sẽ ghép mấy cái đường nét đó lại để nhận ra hình dạng tai, mắt, mũi. Cứ thế, các lớp sâu hơn sẽ bắt đầu nhận ra cả khuôn mặt, bộ lông, dáng đứng... cho đến khi nó "chắc như đinh đóng cột" rằng đây là một con mèo. Hay ho ha?
"""
print(generate(f"{prompt_audio}\n{content}"))