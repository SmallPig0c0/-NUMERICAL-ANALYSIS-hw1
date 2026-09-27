# Numerical Analysis Homework — Problem 7

## 組員資料

- 姓名、學號：邱尹澤 C14111263、鍾秉勳 C14139017、侯品丞 C14096235、莊文泰 C14106153

## 作業內容

實作 `my_interp_plotter(x, y, X, option)`，根據指定的插值方法計算 \(X\) 所對應的 \(Y\)，並畫出原始資料點與插值結果。

本題使用以下三種方法：

- `nearest`：nearest interpolation
- `linear`：linear interpolation
- `cubic`：cubic interpolation

程式未使用 `scipy.interpolate.interp1d`。原始資料點以紅色圓點表示，插值結果以藍色曲線表示，圖中包含標題、座標軸名稱及圖例。

## 檔案說明

- `assignment_07.ipynb`：作業內容、程式執行結果與圖形。
- `interpolation_assignment.py`：插值計算與繪圖程式。
- `test_interpolation_assignment.py`：程式測試。
- `output/`：三種插值方法的輸出圖片。
- `requirements.txt`：執行程式所需套件。

## 執行方式

```powershell
python interpolation_assignment.py
```

執行測試：

```powershell
python -m unittest -v test_interpolation_assignment.py
```

## 繳交內容

繳交的 ZIP 檔包含 Notebook、Python 程式碼及執行結果。
