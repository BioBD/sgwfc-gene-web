from sgwf_gene.settings import ENVIRONMENT


def environment(request):
    data = {}
    data['ENVIRONMENT'] = ENVIRONMENT
    return data
