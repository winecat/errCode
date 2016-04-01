%% ==============================
%% @doc {0}{公用错误码模块}
%% 错误码定义 （与errCode.xml同步）
%% ==============================

-ifndef(ERR_COMMON_HRL).
-define(ERR_COMMON_HRL, ok).	%% ERR_COMMON_HRL START

-define(ERR_COMMON_SUCCEED, 		0).			%% 成功
-define(ERR_COMMON_OPERATE_FAIL,  	2).		%% 操作失败
-define(ERR_COMMON_TYPE_ERROR, 3). 			%% 类型错误

-endif.			%% ERR_COMMON_HRL END