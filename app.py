import streamlit as st
import pickle as pkl
import pandas as pd
from helper.recommender_system import recommender, matrix_display

st.set_page_config(layout="wide")
product_details = pkl.load(open('Product-details.pkl', 'rb'))
similarity_metrix = pkl.load(open('top10 Similar Products.pkl', 'rb'))
# Load product details
try:
    product_details = pd.read_pickle('Product-details.pkl')
except Exception as e:
    st.error(f"Error occurred while loading 'Product-details.pkl': {e}")
    product_details = pd.DataFrame()  # Provide an empty DataFrame in case of error

# Load similarity matrix
# try:
#     similarity_matrix = pkl.load(open('top5 Similar Products.pkl', 'rb'))
# except Exception as e:
#     st.error(f"Error occurred while loading 'top5 Similar Products.pkl': {e}")
#     similarity_matrix = None  # Set to None in case of error

# Load top products index with error handling
try:
    top_products_index = pd.read_pickle('top100_product.pkl')
except Exception as e:
    st.error(f"Error occurred while loading 'top100_product.pkl': {e}")
    top_products_index = pd.DataFrame()  # Provide an empty DataFrame in case of error


# Sidebar
with st.sidebar:
    selected_option = st.selectbox("Type or Select", product_details['name'], index=None,
                                   placeholder='Search Product', )
    search = st.button('Search')

if search:
    if selected_option == None:
        st.warning(' Please select a valid Option', icon='⚠️')
    else:
        st.header(selected_option)
        product, details = st.columns([0.7, 0.3])
        selected_product_index = product_details[product_details['name'] == selected_option].index[0]
        recommended_ids = recommender(selected_product_index, similarity_metrix)

        with product:
            purchase, ratings = st.columns(2)
            with purchase:
                st.image('https://m.media-amazon.com/images/' + product_details.iloc[selected_product_index][
                    'Image url IDS'] + '._AC_UL1500_.jpg', width=450)
                # price
                # with price:
                st.title(f"""Price :blue[{product_details.iloc[selected_product_index]['actual_price']}]""", )
                # st.header(f"""""",)
                # with discount:
                if product_details.iloc[selected_product_index]['discount_price'] != None:
                    st.header('')

                    st.title('Get at only on ')
                    st.header(f""":green[{product_details.iloc[selected_product_index]['discount_price']}]""")
                    url_to_redirect = 'https://www.amazon.in/' + product_details.iloc[selected_product_index][
                        'product Url Ids']
                    st.link_button('Buy Now', url=url_to_redirect)
                    # with buynow:

            with ratings:
                pass

        with details:
            matrix_display(recommended_ids, product_details, 3, 2)
            pass



else:
    matrix_display(top_products_index, product_details, 10, 4)



