import base64
import mimetypes
import os
import re
import struct
from google import genai
from google.genai import types
from dotenv import load_dotenv


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()


def generate(content: str = None):
    if not content:
        return None
    load_dotenv()
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=content),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=[
            "audio",
        ],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Zephyr"
                )
            )
        ),
    )

    file_index = 0
    audio_file_name = None
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"ENTER_FILE_NAME_{file_index}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            if file_extension is None:
                file_extension = ".wav"
                data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)
            full_file_name = f"{file_name}{file_extension}"
            save_binary_file(full_file_name, data_buffer)
            audio_file_name = full_file_name
        else:
            print(chunk.text)
    return audio_file_name

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Generates a WAV file header for the given audio data and parameters.

    Args:
        audio_data: The raw audio data as a bytes object.
        mime_type: Mime type of the audio data.

    Returns:
        A bytes object representing the WAV file header.
    """
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size  # 36 bytes for header fields before data chunk size

    # http://soundfile.sapp.org/doc/WaveFormat/

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    """Parses bits per sample and rate from an audio MIME type string.

    Assumes bits per sample is encoded like "L16" and rate as "rate=xxxxx".

    Args:
        mime_type: The audio MIME type string (e.g., "audio/L16;rate=24000").

    Returns:
        A dictionary with "bits_per_sample" and "rate" keys. Values will be
        integers if found, otherwise None.
    """
    bits_per_sample = 16
    rate = 24000

    # Extract rate from parameters
    parts = mime_type.split(";")
    for param in parts: # Skip the main type part
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                # Handle cases like "rate=" with no value or non-integer value
                pass # Keep rate as default
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass # Keep bits_per_sample as default if conversion fails

    return {"bits_per_sample": bits_per_sample, "rate": rate}


generate("""
Bạn biết không, có đôi khi ngồi nghĩ lại, cái bóng đèn sợi đốt ấy, cái thứ mà chúng ta giờ đây đang dần dẹp vào xó nhà hay chỉ còn thấy lác đác ở mấy quán cà phê hoài cổ, ấy vậy mà nó từng là một cuộc cách mạng đấy. Thật ra mà nói, nó là cái cục đèn điện với một sợi dây kim loại mỏng manh, khi có dòng điện chạy qua thì nóng lên đến mức phát sáng, sáng chói cả một góc nhà. Toàn bộ cái sợi đó, nó nằm gọn gàng bên trong một cái bầu thủy tinh, mà cái bầu này thì hoặc là hút hết không khí ra, hoặc là bơm đầy khí trơ vào, để làm gì ư? Để bảo vệ cái sợi dây quý giá ấy khỏi bị oxy hóa, đơn giản vậy thôi. Dòng điện được đưa tới sợi đốt thông qua mấy cái đầu nối hay dây dẫn được nhúng hẳn vào trong thủy tinh, rồi thì cái đuôi đèn ấy, nó không chỉ giữ chặt bóng đèn mà còn lo luôn cả chuyện kết nối điện nữa.

Ngày xưa, bóng đèn sợi đốt được sản xuất đủ loại kích cỡ, đủ kiểu độ sáng, từ vài von tới tận mấy trăm von lận. Mà cái hay của nó, ôi trời, là chẳng cần bất kỳ thiết bị điều khiển rườm rà nào bên ngoài cả, chi phí sản xuất thì lại thấp, và đặc biệt là dùng được tuốt tuồn tuột từ điện xoay chiều cho đến điện một chiều. Thế nên, chả trách gì mà nó phổ biến khủng khiếp, từ cái nhà bếp nhà mình cho đến mấy cái trung tâm thương mại to đùng, rồi thì mấy cái đèn bàn nhỏ gọn, đèn pha ô tô, đèn pin cầm tay, hay thậm chí là cả mấy cái biển quảng cáo lấp lánh nữa. Cứ chỗ nào cần ánh sáng là y như rằng thấy mặt mũi nó.

Nhưng mà nói thật, cái gì cũng có hai mặt. Bóng đèn sợi đốt này, dù tiện lợi là thế, nhưng nó kém hiệu quả hơn hẳn so với mấy loại đèn điện khác mà chúng ta có bây giờ, bạn biết đấy. Nghe mà ngán ngẩm, chưa đến 5% năng lượng mà nó ngốn vào được chuyển hóa thành ánh sáng nhìn thấy được đâu, còn lại thì sao? Bay hơi thành nhiệt hết, phí ơi là phí. Một cái bóng đèn sợi đốt thông thường, với điện áp 120V, thì hiệu suất phát sáng của nó chỉ vỏn vẹn có 16 lumen trên mỗi watt thôi, trong khi một cái bóng compact huỳnh quang đã là 60 lm/W rồi, còn mấy cái đèn LED trắng hiện đại bây giờ thì có khi lên tới 100 lm/W lận. Nghe con số này thôi là đủ hiểu tại sao chính phủ nhiều nước lại rục rịch cấm đoán dần dần rồi, phải không? Tiêu thụ điện kinh khủng khiếp!

À mà, cũng có những lúc cái "nhược điểm" tỏa nhiệt đó lại biến thành ưu điểm bất ngờ đấy. Chẳng hạn, người ta dùng nó làm đèn sưởi trong lồng ấp cho gà con này, hay trong mấy cái đèn dung nham "lava lamp" trang trí ấy, hoặc là cái lò nướng đồ chơi Easy-Bake Oven mà tụi trẻ con mê tít. Mấy cái lò sưởi hồng ngoại dùng bóng halogen vỏ thạch anh thì lại được tận dụng trong công nghiệp để sấy sơn hay sưởi ấm không gian nữa cơ. Thật là, cái gì cũng có đất dụng võ của nó.

Tuổi thọ của bóng đèn sợi đốt thì thôi rồi, ngắn cũn cỡn so với các loại đèn khác. Một cái bóng đèn gia dụng bình thường thì được khoảng 1.000 giờ thôi, trong khi bóng huỳnh quang compact thì thường là 10.000 giờ, còn mấy ông đèn LED thì bá đạo hơn, tận 20.000-30.000 giờ lận. Bởi vậy, giờ đây, hầu hết bóng đèn sợi đốt đã bị thay thế bởi đèn huỳnh quang, đèn phóng điện cường độ cao, và đặc biệt là đèn LED rồi. Chuyện các chính phủ bắt đầu loại bỏ dần đèn sợi đốt để giảm tiêu thụ năng lượng, đó là điều tất yếu, phải làm thôi, vì tương lai xanh hơn, sạch hơn mà.

Giờ nói về lịch sử một chút đi, cái này mới thú vị này. Robert Friedel và Paul Israel, hai nhà sử học có tiếng, họ đã liệt kê ra bao nhiêu là nhà phát minh bóng đèn sợi đốt trước cả ông Joseph Swan và Thomas Edison của General Electric cơ đấy. Mà họ kết luận, một cách khá dứt khoát là phiên bản của Edison lại vượt trội hơn những người khác là nhờ một sự kết hợp của ba yếu tố chính: thứ nhất là ông ấy tìm được một vật liệu phát sáng hiệu quả, thứ hai là tạo ra được một môi trường chân không cao hơn hẳn những người khác (nhờ sử dụng máy bơm Sprengel), và quan trọng nhất là tạo ra được một cái bóng đèn có điện trở cao, điều này mới giúp cho việc phân phối điện từ một nguồn tập trung trở nên khả thi về mặt kinh tế. Thật sự mà nói, nếu không có cái yếu tố điện trở cao đó, thì có lẽ chúng ta đã không có mạng lưới điện rộng khắp như bây giờ đâu.

Một nhà sử học khác, Thomas Hughes, thì lại quy công lao cho Edison không chỉ vì cái bóng đèn, mà còn vì ông ấy đã phát triển được cả một hệ thống chiếu sáng điện tích hợp hoàn chỉnh. Cái bóng đèn ấy, nó chỉ là một thành phần nhỏ bé trong cả cái "cơ đồ" chiếu sáng điện của ông thôi, và nó cũng chẳng quan trọng hơn gì mấy cái máy phát điện Edison Jumbo, hay đường dây điện chính và đường dây phụ của Edison, rồi cả cái hệ thống phân phối song song nữa. Bạn cứ thử nghĩ xem, bao nhiêu nhà phát minh khác, cũng có máy phát điện, cũng có bóng đèn sợi đốt, và cũng tài tình, xuất sắc không kém gì Edison đâu, nhưng giờ thì họ chìm vào quên lãng hết rồi. Tại sao ư? Bởi vì những người sáng tạo ra họ đã không thể tự mình "dẫn dắt" cái phát minh đó đi vào một hệ thống chiếu sáng hoàn chỉnh. Nghe có vẻ hơi khắc nghiệt nhỉ, nhưng sự thật thì là thế đấy.

Cứ nhìn lại những nghiên cứu tiền thương mại ngày xưa mà xem, bao nhiêu là thử nghiệm, bao nhiêu là công sức đổ vào. Năm 1761, Ebenezer Kinnersley đã thử nghiệm đốt nóng một sợi dây cho nó phát sáng rồi đó. Đến năm 1802, Humphry Davy, sử dụng một "bộ pin khổng lồ" – 2.000 cục pin đặt trong tầng hầm của Royal Institution of Great Britain cơ đấy, để tạo ra ánh sáng sợi đốt bằng cách cho dòng điện chạy qua một dải bạch kim mỏng. Bạch kim được chọn vì nó có điểm nóng chảy cực cao. Nhưng mà, ôi dào, nó chẳng đủ sáng mà cũng chẳng kéo dài được lâu để mà thực tế sử dụng. Tuy nhiên, nó lại là cái khởi nguồn cho nỗ lực của hàng loạt các nhà thực nghiệm trong suốt 75 năm tiếp theo đấy.

Trong suốt ba phần tư đầu thế kỷ 19, rất nhiều nhà thực nghiệm đã miệt mài với đủ các sự kết hợp giữa dây bạch kim hoặc iridi, các thanh carbon, và các khoang chân không hoặc bán chân không. Nhiều thiết bị trong số này đã được trình diễn, và một số thì được cấp bằng sáng chế nữa. Năm 1835, James Bowman Lindsay đã trình diễn một ánh sáng điện ổn định tại một buổi họp công cộng ở Dundee, Scotland. Ông ấy khoe rằng có thể "đọc sách ở khoảng cách một mét rưỡi". Tiếc thay, ông lại không phát triển cái đèn điện đó thêm nữa. Đến năm 1838, Marcellin Jobard, một nhà in thạch bản người Bỉ, đã phát minh ra một bóng đèn sợi đốt với môi trường chân không sử dụng sợi carbon.

Năm 1840, nhà khoa học người Anh Warren De la Rue đã bọc một sợi bạch kim xoắn trong một ống chân không và cho dòng điện chạy qua. Thiết kế này dựa trên ý tưởng rằng điểm nóng chảy cao của bạch kim sẽ cho phép nó hoạt động ở nhiệt độ cao, và khoang chân không sẽ chứa ít phân tử khí hơn để phản ứng với bạch kim, từ đó cải thiện tuổi thọ của nó. Mặc dù là một thiết kế khả thi, nhưng chi phí của bạch kim lại khiến nó không thực tế cho việc sử dụng thương mại. Thế rồi, năm 1841, Frederick de Moleyns từ Anh được cấp bằng sáng chế đầu tiên cho một bóng đèn sợi đốt, với thiết kế sử dụng dây bạch kim nằm trong một bầu chân không. Ông này cũng dùng cả carbon nữa.

Rồi đến năm 1845, John W. Starr, một người Mỹ, đã được cấp bằng sáng chế cho một bóng đèn sợi đốt sử dụng sợi carbon. Nhưng cái phát minh của ông thì chẳng bao giờ được sản xuất thương mại cả. Năm 1851, Jean Eugène Robert-Houdin đã công khai trình diễn các bóng đèn sợi đốt tại điền trang của mình ở Blois, Pháp. Mấy cái bóng đèn của ông ấy giờ vẫn còn được trưng bày trong bảo tàng ở Château de Blois đấy. Năm 1859, Moses G. Farmer đã chế tạo một bóng đèn sợi đốt điện sử dụng sợi bạch kim. Sau này, Thomas Edison đã nhìn thấy một trong những bóng đèn này trong một cửa hàng ở Boston và thậm chí còn hỏi Farmer xin lời khuyên về việc kinh doanh đèn điện nữa cơ.

Năm 1872, Alexander Lodygin người Nga đã phát minh ra một bóng đèn sợi đốt và được cấp bằng sáng chế tại Nga vào năm 1874. Ông này sử dụng hai thanh carbon với tiết diện giảm dần trong một ống thủy tinh được bịt kín, chứa đầy nitơ, được sắp xếp điện sao cho dòng điện có thể chuyển sang thanh carbon thứ hai khi thanh thứ nhất đã bị đốt cháy hết. Sau này ông sang Mỹ, đổi tên thành Alexander de Lodyguine và nộp đơn xin, rồi được cấp bằng sáng chế cho các loại đèn sợi đốt có sợi crom, iridi, rhodi, rutheni, osmi, molypden và vonfram. Thậm chí một cái bóng đèn sử dụng sợi molypden còn được trình diễn tại hội chợ thế giới năm 1900 ở Paris nữa cơ.

Ngày 24 tháng 7 năm 1874, một bằng sáng chế Canada đã được nộp bởi Henry Woodward và Mathew Evans cho một loại đèn bao gồm các thanh carbon được gắn trong một xi lanh thủy tinh chứa đầy nitơ. Họ không thành công trong việc thương mại hóa loại đèn của mình, và đã bán quyền sáng chế (Bằng sáng chế Hoa Kỳ 181,613) cho Thomas Edison vào năm 1879. Có vẻ như Edison cần quyền sở hữu đối với tuyên bố mới lạ về các loại đèn được kết nối song song, ấy là cái mấu chốt đấy.

Đến ngày 4 tháng 3 năm 1880, chỉ năm tháng sau khi bóng đèn của Edison ra đời, Alessandro Cruto đã tạo ra chiếc đèn sợi đốt đầu tiên của mình. Cruto đã tạo ra một sợi đốt bằng cách lắng đọng than chì trên các sợi bạch kim mỏng, bằng cách đốt nóng nó bằng dòng điện khi có mặt khí ethyl alcohol. Đốt nóng bạch kim ở nhiệt độ cao sẽ để lại các sợi bạch kim mỏng được phủ than chì tinh khiết. Đến tháng 9 năm 1881, ông ấy đã đạt được một phiên bản thành công của sợi đốt tổng hợp đầu tiên. Bóng đèn do Cruto phát minh kéo dài tới 500 giờ, so với chỉ 40 giờ của phiên bản gốc của Edison. Tại Triển lãm Điện Munich năm 1882 ở Bavaria, Đức, đèn của Cruto hiệu quả hơn đèn của Edison và tạo ra ánh sáng trắng, đẹp hơn hẳn.

Năm 1893, Heinrich Göbel tuyên bố rằng ông đã thiết kế bóng đèn sợi đốt đầu tiên vào năm 1854, với sợi tre carbon hóa mỏng có điện trở cao, dây dẫn bạch kim trong một vỏ hoàn toàn bằng thủy tinh, và chân không cao. Các thẩm phán của bốn tòa án đã bày tỏ nghi ngờ về tuyên bố của Göbel, nhưng không bao giờ có một quyết định cuối cùng do bằng sáng chế của Edison đã hết hạn. Một công trình nghiên cứu được công bố vào năm 2007 đã kết luận rằng câu chuyện về những chiếc đèn của Göbel vào những năm 1850 là hư cấu. Thật là lắm drama, phải không?

Giờ đến giai đoạn thương mại hóa, đây mới là lúc mọi thứ bùng nổ đây. Joseph Swan (1828–1914), một nhà vật lý và hóa học người Anh, đã bắt đầu nghiên cứu với sợi giấy carbon hóa trong một bầu thủy tinh chân không vào năm 1850. Đến năm 1860, ông ấy đã có thể trình diễn một thiết bị hoạt động được, nhưng do thiếu một môi trường chân không tốt và nguồn cung cấp điện đầy đủ nên bóng đèn có tuổi thọ ngắn và nguồn sáng không hiệu quả. Đến giữa những năm 1870, các loại máy bơm tốt hơn đã xuất hiện, và Swan quay lại với các thí nghiệm của mình.

Với sự giúp đỡ của Charles Stearn, một chuyên gia về máy bơm chân không, vào năm 1878, Swan đã phát triển một phương pháp xử lý giúp tránh được hiện tượng bóng đèn bị đen sớm. Phương pháp này đã được cấp bằng sáng chế của Anh vào năm 1880. Ngày 18 tháng 12 năm 1878, một chiếc đèn sử dụng thanh carbon mỏng đã được trình diễn tại một cuộc họp của Hội Hóa học Newcastle, và Swan đã thực hiện một màn trình diễn thực tế tại cuộc họp của họ vào ngày 17 tháng 1 năm 1879. Nó cũng được trình diễn cho 700 người tham dự một cuộc họp của Hội Văn học và Triết học Newcastle upon Tyne vào ngày 3 tháng 2 năm 1879. Những chiếc đèn này sử dụng thanh carbon từ đèn hồ quang chứ không phải sợi mỏng. Vì vậy chúng có điện trở thấp và yêu cầu dây dẫn rất lớn để cung cấp dòng điện cần thiết, nên chúng không thực tế về mặt thương mại, mặc dù chúng đã chứng minh được khả năng của đèn sợi đốt với chân không tương đối cao, dây dẫn carbon và dây dẫn bạch kim. Chiếc bóng đèn này kéo dài khoảng 40 giờ.

Sau đó, Swan chuyển sự chú ý của mình sang việc sản xuất một sợi carbon tốt hơn và phương tiện để gắn các đầu của nó. Ông đã nghĩ ra một phương pháp xử lý bông để tạo ra "sợi giấy da" vào đầu những năm 1880 và được cấp bằng sáng chế Anh số 4933 cùng năm đó. Từ năm này, ông bắt đầu lắp đặt bóng đèn trong các ngôi nhà và địa danh ở Anh. Ngôi nhà của ông, Underhill, Low Fell, Gateshead, là ngôi nhà đầu tiên trên thế giới được chiếu sáng bằng bóng đèn. Vào đầu những năm 1880, ông đã thành lập công ty của mình. Năm 1881, Nhà hát Savoy ở Thành phố Westminster, Luân Đôn đã được chiếu sáng bằng bóng đèn sợi đốt của Swan, đây là nhà hát đầu tiên, và là tòa nhà công cộng đầu tiên trên thế giới, được chiếu sáng hoàn toàn bằng điện. Con đường đầu tiên trên thế giới được chiếu sáng bằng bóng đèn sợi đốt là phố Mosley, Newcastle upon Tyne, Vương quốc Anh. Nó được chiếu sáng bằng đèn sợi đốt của Joseph Swan vào ngày 3 tháng 2 năm 1879.

Thomas Edison thì, như chúng ta đã biết, bắt đầu nghiên cứu nghiêm túc để phát triển một chiếc đèn sợi đốt thực tế vào năm 1878. Edison đã nộp đơn xin cấp bằng sáng chế đầu tiên cho "Cải tiến trong đèn điện" vào ngày 14 tháng 10 năm 1878. Sau rất nhiều thí nghiệm, ban đầu với carbon vào đầu những năm 1880 và sau đó với bạch kim và các kim loại khác, cuối cùng Edison đã quay lại với sợi carbon. Cuộc thử nghiệm thành công đầu tiên là vào ngày 22 tháng 10 năm 1879, và kéo dài 13.5 giờ. Edison tiếp tục cải tiến thiết kế này và đến ngày 4 tháng 11 năm 1879, đã nộp đơn xin cấp bằng sáng chế Hoa Kỳ cho một chiếc đèn điện sử dụng "một sợi hoặc dải carbon cuộn lại và nối... với dây tiếp xúc bạch kim." Mặc dù bằng sáng chế mô tả một số cách tạo sợi carbon bao gồm sử dụng "chỉ bông và lanh, thanh gỗ mỏng, giấy cuộn theo nhiều cách khác nhau," Edison và nhóm của ông sau đó đã phát hiện ra rằng một sợi tre carbon hóa có thể kéo dài hơn 1200 giờ. Năm 1880, con tàu hơi nước Columbia của Công ty Đường sắt và Hàng hải Oregon, đã trở thành ứng dụng đầu tiên cho đèn điện sợi đốt của Edison (nó cũng là con tàu đầu tiên sử dụng máy phát điện dynamo).

Albon Man, một luật sư New York, đã thành lập Công ty Chiếu sáng Điện Electro-Dynamic vào năm 1878 để khai thác các bằng sáng chế của mình và của William Sawyer. Vài tuần sau, Công ty Chiếu sáng Điện Hoa Kỳ được thành lập. Công ty này không thực hiện lắp đặt đèn sợi đốt thương mại đầu tiên cho đến mùa thu năm 1880, tại Công ty Két sắt Mercantile ở Thành phố New York, khoảng sáu tháng sau khi đèn sợi đốt của Edison được lắp đặt trên tàu Columbia. Hiram S. Maxim là kỹ sư trưởng tại Công ty Chiếu sáng Điện Hoa Kỳ. Sau thành công lớn ở Hoa Kỳ, bóng đèn sợi đốt được cấp bằng sáng chế bởi Edison cũng bắt đầu trở nên phổ biến rộng rãi ở châu Âu; trong số những nơi khác, những chiếc bóng đèn Edison đầu tiên ở các nước Bắc Âu đã được lắp đặt tại xưởng dệt của nhà máy dệt Finlayson ở Tampere, Phần Lan vào tháng 3 năm 1882.

Lewis Latimer, lúc đó đang làm việc cho Edison, đã phát triển một phương pháp cải tiến để xử lý nhiệt sợi carbon giúp giảm gãy vỡ và cho phép chúng được đúc thành các hình dạng mới lạ, chẳng hạn như hình chữ "M" đặc trưng của sợi Maxim. Ngày 17 tháng 1 năm 1882, Latimer đã nhận được bằng sáng chế cho "Quy trình sản xuất carbon", một phương pháp cải tiến để sản xuất sợi bóng đèn, sau đó được Công ty Chiếu sáng Điện Hoa Kỳ mua lại. Latimer đã cấp bằng sáng chế cho các cải tiến khác như một cách tốt hơn để gắn sợi vào giá đỡ dây của chúng.

Ở Anh, các công ty Edison và Swan đã sáp nhập thành Công ty Điện United Edison và Swan (sau này được gọi là Ediswan, và cuối cùng được sáp nhập vào Thorn Lighting Ltd). Edison ban đầu chống lại sự kết hợp này, nhưng cuối cùng Edison buộc phải hợp tác và việc sáp nhập đã được thực hiện. Cuối cùng, Edison đã mua lại tất cả quyền lợi của Swan trong công ty. Swan đã bán quyền sáng chế của mình tại Hoa Kỳ cho Công ty Điện Brush vào tháng 6 năm 1882.

Văn phòng Bằng sáng chế Hoa Kỳ đã đưa ra phán quyết vào ngày 8 tháng 10 năm 1883, rằng các bằng sáng chế của Edison dựa trên kỹ thuật đã có trước của William Sawyer và không hợp lệ. Các vụ kiện tụng tiếp tục trong một số năm. Cuối cùng vào ngày 6 tháng 10 năm 1889, một thẩm phán đã phán quyết rằng tuyên bố cải tiến đèn điện của Edison về "một sợi carbon có điện trở cao" là hợp lệ.

Nói tóm lại, cái bóng đèn sợi đốt ấy, nó không chỉ là một phát minh đơn thuần đâu, mà nó còn là cả một câu chuyện dài với biết bao nhiêu bộ óc vĩ đại, bao nhiêu công sức đổ mồ hôi sôi nước mắt, bao nhiêu cuộc tranh cãi pháp lý nảy lửa nữa. Dù giờ đây nó đang dần nhường chỗ cho những công nghệ mới hơn, hiệu quả hơn, nhưng không thể phủ nhận rằng nó đã từng thắp sáng cả một kỷ nguyên, mở ra một chương mới cho cuộc sống nhân loại. Nó là biểu tượng của sự kiên trì, của tinh thần sáng tạo không ngừng nghỉ, và cả những bài học đắt giá về tầm quan trọng của một hệ thống tổng thể, chứ không chỉ riêng một bộ phận, bạn nhỉ?
""")