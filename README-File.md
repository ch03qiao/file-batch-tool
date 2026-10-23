# 📁 文件批量整理工具（归档·重命名·加序号）

> 人工智专业在校接单作品 · 把杂乱文件夹一键收拾整齐。
> **零依赖**：只用 Python 标准库，不装任何包就能跑。

![Python](https://img.shields.io/badge/Python-标准库-3776AB?logo=python&logoColor=white)
![No deps](https://img.shields.io/badge/dependencies-0-brightgreen)

---

## ✨ 功能

- 🗂 **按类型归档**：自动建 `pdf文件/`、`png文件/`、`xlsx文件/` 等子文件夹
- 🔤 **空格转下划线**：`月度销售 report.txt` → `月度销售_report.txt`
- ➕ **批量加前缀/序号**：`001_奶茶_IMG_001.PNG`
- ♻️ **改后缀**：可批量把 `.jpeg` 统一成 `.jpg`

---

## 🚀 快速开始

```bash
# 零依赖，直接跑
python 示例3_文件批量处理.py 杂乱文件夹 --archive --space-to-underscore --prefix 奶茶_ --serial

# 只重命名（不移动）
python 示例3_文件批量处理.py 文件夹 --space-to-underscore --prefix 项目_ --serial
```

### 参数说明
| 参数 | 说明 |
|---|---|
| `--archive` | 按扩展名归档到子文件夹 |
| `--space-to-underscore` | 空格替换为下划线 |
| `--prefix 文本` | 文件名加前缀 |
| `--serial` | 加两位序号前缀 |
| `--ext 新后缀` | 批量改扩展名 |

---

## 📸 效果演示

**输入**（10 个乱序文件）：
```
IMG_001.PNG  data(1).csv  产品图备份.JPEG  会议记录.pdf  ...
```
**输出**（归档 + 规范命名）：
```
png文件/001_奶茶_IMG_001.PNG
csv文件/002_奶茶_data(1).csv
pdf文件/006_奶茶_会议记录.pdf
...
```

---

## 💼 接单场景

- 毕业/项目资料整理交付
- 电商素材按类归档
- 批量文件规范化命名

📩 接单联系见 [个人主页](https://github.com/ch03qiao)。
