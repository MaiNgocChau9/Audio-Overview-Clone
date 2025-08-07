import os
from pathlib import Path
from typing import List, Tuple, Optional

def display_files_table(files: List[Path]) -> None:
    """Hiển thị danh sách file dưới dạng bảng đẹp mắt"""
    print(f"\n{'╭':<1}{'─' * 78}{'╮'}")
    print(f"│ {'STT':<4} │ {'TÊN FILE':<40} │ {'KÍCH THƯỚC':<12} │ {'LOẠI':<15} │")
    print(f"│{'─' * 6}┼{'─' * 42}┼{'─' * 14}┼{'─' * 17}│")
    
    for idx, file_path in enumerate(files, 1):
        try:
            file_size = file_path.stat().st_size
            size_str = format_file_size(file_size)
            file_ext = file_path.suffix.upper() or "Không xác định"
            file_name = file_path.name
            
            # Cắt tên file nếu quá dài
            if len(file_name) > 40:
                file_name = file_name[:37] + "..."
                
            print(f"│ {idx:<4} │ {file_name:<40} │ {size_str:<12} │ {file_ext:<15} │")
            
        except Exception:
            print(f"│ {idx:<4} │ {file_path.name:<40} │ {'Lỗi':<12} │ {'Lỗi':<15} │")
    
    print(f"{'╰':<1}{'─' * 78}{'╯'}")

def format_file_size(size_bytes: int) -> str:
    """Chuyển đổi byte thành định dạng dễ đọc"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.1f}MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.1f}GB"

def parse_selection(selection: str, max_files: int) -> List[int]:
    """
    Phân tích chuỗi lựa chọn thành danh sách số
    Hỗ trợ: 1,2,3 hoặc 1-5 hoặc kết hợp 1,3-5,7
    """
    selected_indices = set()
    
    try:
        # Tách theo dấu phẩy
        parts = [part.strip() for part in selection.split(',')]
        
        for part in parts:
            if '-' in part:
                # Xử lý range như 1-5
                start, end = part.split('-', 1)
                start_idx = int(start.strip())
                end_idx = int(end.strip())
                
                if 1 <= start_idx <= max_files and 1 <= end_idx <= max_files:
                    for i in range(min(start_idx, end_idx), max(start_idx, end_idx) + 1):
                        selected_indices.add(i)
                else:
                    raise ValueError(f"Số nằm ngoài phạm vi: {part}")
            else:
                # Xử lý số đơn lẻ
                idx = int(part.strip())
                if 1 <= idx <= max_files:
                    selected_indices.add(idx)
                else:
                    raise ValueError(f"Số nằm ngoài phạm vi: {idx}")
    
    except ValueError as e:
        raise ValueError(f"Định dạng không hợp lệ: {e}")
    
    return sorted(list(selected_indices))

def choose_files_and_content() -> Tuple[List[str], List[str]]:
    """
    Cho phép người dùng chọn nhiều file từ thư mục và đọc nội dung.
    
    Returns:
        tuple: (danh_sách_đường_dẫn, danh_sách_nội_dung)
    """
    print("╔" + "═" * 50 + "╗")
    print("║" + " " * 20 + "CHỌN FILE " + " " * 20 + "║")
    print("╚" + "═" * 50 + "╝")
    
    # Nhập đường dẫn thư mục
    while True:
        path = input("\n📁 Nhập đường dẫn thư mục (Enter để thoát): ").strip()
        
        if not path:
            print("👋 Thoát chương trình.")
            return [], []

        path_obj = Path(path)
        
        if not path_obj.exists():
            print(f"❌ Đường dẫn '{path}' không tồn tại. Vui lòng thử lại.")
            continue
        
        if not path_obj.is_dir():
            print(f"❌ '{path}' không phải là thư mục. Vui lòng thử lại.")
            continue
            
        break

    # Lấy danh sách file
    try:
        files = [f for f in path_obj.iterdir() if f.is_file()]
        
        if not files:
            print("❌ Không tìm thấy file nào trong thư mục.")
            return [], []

        # Sắp xếp theo tên
        files.sort(key=lambda x: x.name.lower())
        
        # Hiển thị bảng file
        print(f"\n📋 Tìm thấy {len(files)} file:")
        display_files_table(files)
        
        # Hướng dẫn chọn file
        print("\n💡 CÁCH CHỌN FILE:")
        print("   • Chọn 1 file: 1")
        print("   • Chọn nhiều file: 1,3,5")
        print("   • Chọn dải file: 1-5")
        print("   • Kết hợp: 1,3-5,7")
        print("   • Chọn tất cả: all")
        
        # Cho người dùng chọn file
        while True:
            try:
                selection = input(f"\n🎯 Chọn file (1-{len(files)}): ").strip().lower()
                
                if not selection:
                    print("❌ Vui lòng nhập lựa chọn.")
                    continue
                
                if selection == "all":
                    selected_indices = list(range(1, len(files) + 1))
                else:
                    selected_indices = parse_selection(selection, len(files))
                
                if not selected_indices:
                    print("❌ Không có file nào được chọn.")
                    continue
                
                break
                
            except ValueError as e:
                print(f"❌ {e}. Vui lòng thử lại.")

        # Hiển thị file đã chọn
        selected_files = [files[i-1] for i in selected_indices]
        print(f"\n✅ Đã chọn {len(selected_files)} file:")
        for i, file_path in enumerate(selected_files, 1):
            print(f"   {i}. {file_path.name}")

        # Đọc nội dung các file
        file_paths = []
        file_contents = []
        
        print(f"\n📖 Đang đọc nội dung...")
        
        for file_path in selected_files:
            try:
                # Thử đọc với UTF-8 trước
                content = read_file_content(file_path)
                file_paths.append(str(file_path))
                file_contents.append(content)
                print(f"   ✓ {file_path.name}")
                
            except Exception as e:
                print(f"   ❌ Lỗi đọc {file_path.name}: {e}")
                continue

        # Tùy chỉnh nội dung (tùy chọn)
        print(f"\n🔧 Tùy chỉnh nội dung:")
        customize = input("   Nhập nội dung tùy chỉnh (Enter để bỏ qua): ").strip()
        
        if customize:
            # Thay thế tất cả nội dung bằng nội dung tùy chỉnh
            file_contents = [customize] * len(file_contents)
            print("   ✓ Đã áp dụng nội dung tùy chỉnh cho tất cả file")

        return file_paths, file_contents

    except PermissionError:
        print(f"❌ Không có quyền truy cập vào thư mục '{path}'.")
        return [], []
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")
        return [], []

def read_file_content(file_path: Path) -> str:
    """Đọc nội dung file với nhiều encoding"""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    # Nếu tất cả encoding đều thất bại, đọc dưới dạng binary
    with open(file_path, 'rb') as f:
        binary_content = f.read()
        return f"[Binary file - {len(binary_content)} bytes]"

def main():
    """Hàm chính để test"""
    file_paths, contents = choose_files_and_content()
    
    if file_paths:
        print(f"\n{'='*60}")
        print(f"KỂT QUẢ: ĐÃ CHỌN {len(file_paths)} FILE")
        print(f"{'='*60}")
        
        for i, (file_path, content) in enumerate(zip(file_paths, contents), 1):
            print(f"\n📄 FILE {i}: {Path(file_path).name}")
            print(f"📍 Đường dẫn: {file_path}")
            print("─" * 40)
            
            # Hiển thị preview nội dung
            if len(content) > 300:
                print(content[:300])
                print(f"\n... (và {len(content) - 300} ký tự nữa)")
            else:
                print(content)
            
            if i < len(file_paths):
                print("\n" + "="*40)
    else:
        print("\n❌ Không có file nào được chọn hoặc xảy ra lỗi.")

if __name__ == "__main__":
    main()