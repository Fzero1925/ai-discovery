# AI Discovery 闈欐€佺珯鐐?

AI Discovery 鏄仛鐒?鈥淎I 鏂伴椈 + AI 宸ュ叿鎸囧崡 + 鏈哄櫒浜轰笓棰樷€?鐨勮嫳鏂囧唴瀹圭珯锛岀洰鏍囨槸閫氳繃 Google AdSense 瀹炵幇闀挎湡鍙樼幇銆傜敓浜т粨搴撲粎淇濈暀 Hugo 闈欐€佺珯鐐瑰繀闇€鏂囦欢锛屽悗鏈熺淮鎶ゅ彧闇€涓婁紶绗﹀悎妯℃澘鐨?Markdown 鍐呭鍗冲彲銆?

- **鏍稿績鏍忕洰**锛歚News`锛堟柊闂诲揩璁笌娣卞害瑙ｈ锛夈€乣Tools`锛圓I 宸ュ叿璇勬祴涓庢鍗曪級銆乣Robot`锛堝伐涓?鏈嶅姟鏈哄櫒浜轰笓棰橈級銆乣About`锛堝搧鐗屼俊鎭級銆?
- **杩愯惀绛栫暐**锛氫繚鎸侀珮璐ㄩ噺鑻辨枃鍐呭銆佸悎娉曞悎瑙勭殑鍥剧墖涓庣粨鏋勫寲鏁版嵁鏀寔锛屾彁鍗?CPC 涓庢敹褰曟晥鏋溿€?
- **瀵艰埅閰嶇疆**锛氳 `config.toml`锛岃彍鍗曢『搴忎负 News 鈫?Tools 鈫?Robot 鈫?About銆?

## 蹇€熷紑濮?

```bash
# 鍏嬮殕浠撳簱
git clone https://github.com/yourusername/ai-discovery.git
cd ai-discovery

# 瀹夎渚濊禆锛堜粎闇€ Hugo锛屽鏋滈渶瑕?Tailwind 鑷畾涔夊垯瀹夎 Node锛?
npm install

# 鏈湴棰勮
hugo server -D
```

> 澶囨敞锛氭墍鏈夎嚜鍔ㄥ寲鑴氭湰銆佹暟鎹鐞嗐€佺洃鎺у伐鍏峰凡杩佺Щ鑷充粨搴撳鐨?`../ai-discovery-automation/` 鐩綍锛屽闇€鎵归噺鐢熸垚鍐呭锛屽彲鍦ㄦ湰鍦版垨绉佹湁鐜涓繍琛岋紝鍐嶅皢鐢熸垚鐨?Markdown 鎷疯礉鍥炴湰浠撳簱 `content/`銆?

## 鍐呭鍙戝竷娴佺▼锛堥浂缁存姢锛?

1. 鍑嗗 Markdown 鏂囦欢锛岃ˉ鍏?front matter锛?
   ```yaml
   ---
   title: "绀轰緥鏍囬"
   description: "150 瀛椾互鍐呮憳瑕?
   date: 2025-09-20
   categories: ["news"]
   tags: ["ai", "robotics"]
   featured_image: "/images/sample.jpg"
   image_alt: "鎻忚堪鍥剧墖鍐呭"
   draft: false
   ---
   ```
2. 所有 Markdown 文章统一放入 `content/articles/`，并通过 front matter 的 `categories` 字段控制导航与列表归属（如 `news`, `robotics`, `content-creation`）。
   - 鏈哄櫒浜轰笓棰?鈫?`content/robot/`锛堝彲鎸?`industrial/`銆乣service/`銆乣research/` 寤哄瓙鐩綍锛?
3. 鎻愪氦骞舵帹閫侊紝Vercel 鑷姩鏋勫缓鍙戝竷銆?

## 鐩綍缁撴瀯

```
ai-discovery/
鈹溾攢鈹€ content/            # News / Tools / Robot / About 绛?Markdown 鍐呭
鈹溾攢鈹€ layouts/            # Hugo 妯℃澘锛堥椤点€佸垪琛ㄣ€佸崟椤点€乸artials 绛夛級
鈹溾攢鈹€ static/             # 闈欐€佽祫婧愶紙CSS/JS/鍥剧墖锛?
鈹溾攢鈹€ config/             # 绔欑偣閰嶇疆琛ュ厖鏂囦欢
鈹溾攢鈹€ dev-docs/           # 鍐呴儴瑙勫垝鏂囨。锛堝凡鍔犲叆 .gitignore锛屼笉鎺ㄩ€?GitHub锛?
鈹溾攢鈹€ config.toml         # Hugo 涓婚厤缃?
鈹溾攢鈹€ README.md           # 鏈枃妗?
鈹斺攢鈹€ vercel.json         # 閮ㄧ讲閰嶇疆
```

## 鏈哄櫒浜烘爮鐩鏄?

- 璁块棶 `/robot/` 鍗冲彲鏌ョ湅鏈哄櫒浜轰笓棰橀〉锛岄〉闈㈡彁渚涗簡 `Industrial`, `Service`, `Research` 涓変釜閿氱偣锛屼究浜庡畾浣嶅唴瀹广€?
- 涓婁紶鍐呭鏃跺皢 Markdown 鏀惧叆瀵瑰簲瀛愮洰褰曪紝Hugo 浼氬熀浜?front matter 鑷姩褰掓。骞剁敓鎴愰〉闈€?

## SEO 涓庡悎瑙?

- 妯℃澘鍐呯疆缁撴瀯鍖栨暟鎹€侀潰鍖呭睉銆佺珯鐐瑰湴鍥俱€丩azy Load 绛?SEO 鑳藉姏锛屾棤闇€棰濆鑴氭湰銆?
- 涓婁紶鍥剧墖鏃惰纭鐗堟潈涓庢潵婧愶紝骞惰ˉ鍏?`image_alt` 鏂囨湰銆?
- `About` 椤甸潰寤鸿鎻愪緵鍝佺墝鎻忚堪銆佽仈绯绘柟寮忋€侀殣绉?鏉℃閾炬帴锛屾弧瓒?AdSense 瀹℃牳瑕佹眰銆?

## 甯歌鍛戒护

```bash
hugo server -D          # 鏈湴棰勮
hugo --minify           # 鐢熸垚鐢熶骇鐜闈欐€佹枃浠讹紙杈撳嚭鍒?public/锛?
```

鏇村鍐呴儴璁″垝銆佽矾绾垮浘涓庡緟鍔炰簨椤硅瑙?`dev-docs/` 鐩綍涓殑 Markdown 鏂囦欢锛堜粎渚涘洟闃熷弬鑰冿級銆?
