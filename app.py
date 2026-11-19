import streamlit as st
import pandas as pd
from collections import Counter
from rapidfuzz import fuzz
from src.name_cleaner import clean_product_name, display_product_name

st.set_page_config(
    page_title="Products Name Cleaner",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Products Name Cleaner")
st.write("上传商品名称 Excel 文件，清洗名称、识别重复商品并导出结果。")

uploaded_file = st.file_uploader(
    "上传 Excel 文件（.xlsx）",
    type=["xlsx"]
)

similarity_threshold = st.slider(
    "相似度阈值",
    min_value=80,
    max_value=100,
    value=92
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("原始数据预览")
    st.dataframe(df.head(10))

    column = st.selectbox(
        "请选择商品名称所在列",
        options=df.columns
    )

    if st.button("开始清洗", type="primary"):
        result = df.copy()

        result["原始名称"] = result[column].fillna("").astype(str)
        result["清洗后名称"] = result["原始名称"].apply(
            clean_product_name
        )
        result["标准化名称"] = result["原始名称"].apply(
            display_product_name
        )

        counts = Counter(result["标准化名称"])

        result["出现次数"] = result["标准化名称"].map(counts)

        unique_names = result[
            ["标准化名称", "清洗后名称"]
        ].drop_duplicates()

        unique_names = unique_names.reset_index(drop=True)

        canonical_names = unique_names["标准化名称"].tolist()
        matched = {}
        review_rows = []

        progress = st.progress(0)
        total = len(canonical_names)

        for i, name in enumerate(canonical_names):
            if name in matched:
                progress.progress((i + 1) / total)
                continue

            matched[name] = name

            for candidate in canonical_names[i + 1:]:
                if candidate in matched:
                    continue

                score = fuzz.ratio(name, candidate)

                if score >= similarity_threshold:
                    review_rows.append({
                        "名称A": name,
                        "名称B": candidate,
                        "相似度": score,
                        "建议": "需要人工确认"
                    })

            progress.progress((i + 1) / total)

        result["匹配状态"] = "待人工确认"
        result.loc[
            result["清洗后名称"] == "",
            "匹配状态"
        ] = "空名称"

        standard_library = (
            result[result["清洗后名称"] != ""]
            .groupby("标准化名称", as_index=False)
            .agg(
                商品名称=("标准化名称", "first"),
                原始名称数量=("原始名称", "nunique"),
                出现总次数=("原始名称", "size")
            )
        )

        review = pd.DataFrame(review_rows)

        st.success("清洗完成！")

        col1, col2, col3 = st.columns(3)
        col1.metric("原始记录数", len(result))
        col2.metric("标准化名称数", len(standard_library))
        col3.metric("待审核相似组合", len(review))

        st.subheader("标准商品库")
        st.dataframe(standard_library, use_container_width=True)

        st.subheader("原始名称映射表")
        st.dataframe(result, use_container_width=True)

        st.subheader("相似名称人工审核")
        if len(review) > 0:
            st.dataframe(review, use_container_width=True)
        else:
            st.info("没有发现达到当前相似度阈值的名称组合。")

        output = __import__("io").BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            standard_library.to_excel(
                writer, sheet_name="标准商品库", index=False
            )
            result.to_excel(
                writer, sheet_name="原始名称映射表", index=False
            )
            review.to_excel(
                writer, sheet_name="相似名称审核", index=False
            )

        st.download_button(
            label="下载清洗结果 Excel",
            data=output.getvalue(),
            file_name="商品名称清洗结果.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("请先上传 Excel 文件。Excel 中需要有一列商品名称。")
