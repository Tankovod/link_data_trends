import pandas as pd
import matplotlib.pyplot as plt


def pd_view_data(data):
    data = pd.DataFrame(data)
    plt.scatter(pd.to_datetime(data['dt']), data['name'], c=data['ping'], s=5)
    manager = plt.get_current_fig_manager()
    manager.resize(1280, 900)
    plt.grid(color='black', alpha=0.1)
    plt.title('Тренды связи с объектами')
    plt.show()
