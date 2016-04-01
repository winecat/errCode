-module(erlcode).-export[info/1].

info(_ErrCode = 0) -> <<"成功">>;
info(_ErrCode = 2) -> <<"操作失败">>;
info(_ErrCode = 3) -> <<"类型错误">>;
info(_) -> <<>>.
