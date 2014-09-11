## -*- coding: utf-8 -*-
<html>
	<head>
		<style type="text/css">
		@font-face {
			font-family: "bvrocrb";
			font-style: normal;
			font-weight: normal;
			src: url(${police_absolute_path('ocrbb.ttf')}) format("truetype");
		}

		#ocrbb{
			position:absolute;
			left:${str(company.bvr_scan_line_horz or '0.0').replace(',','.')}mm;
			top:${str(company.bvr_scan_line_vert or '0.0').replace(',','.')}mm;
			font-family:bvrocrb;
			font-size:${str(company.bvr_scan_line_font_size or '0.0').replace(',','.')}pt;
			text-align:left;
			width: 119mm;
		}

		.digitref {
			position:absolute;
			top:7px;
			text-align:center;
			float:left;
			width:9px;
		}

		.slip_address_b {
			position:absolute;
            top:${str(62 + (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(5 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}

		.dest_address_bvr {
			position:absolute;
			top:${str(company.bvr_add_vert or '0.0').replace(',','.')}mm;
			left:${str(company.bvr_add_horz or '0.0').replace(',','.')}mm;
			font-size:12;
			text-align:left;
		}

		.slip_bank_acc {
			font-family:Helvetica;
			font-size:8pt;
			border-width:0px;
			padding-left:0mm;
			padding-top:0mm;
			position:absolute;
			top:${str(42 + (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(30 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}

		.slip_bank_add_acc {
			font-family:Helvetica;
			font-size:8pt;
			border-width:0px;
			padding-left:0mm;
			padding-top:0mm;
			position:absolute;
			top:${str(160 + (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(5 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}

		.slip_comp {
			font-family:Helvetica;
			font-size:8pt;
			border-width:0px;
			padding-left:0mm;
			padding-top:0mm;
			position:absolute;
			top:${str(10+ (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(7 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}

		.slip_add {
			font-family:Helvetica;
			font-size:8pt;
			border-width:0px;
			padding-left:0mm;
			padding-top:0mm
		}

		.slip_amount {
			width:5cm;
			text-align:right;
			font-size:11pt;
			font-family:Helvetica;
			position:absolute;
			top:${str(50 + (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(7 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}

		/*
		Slip 2 element
		*/

		.slip2_address_b {
			position:absolute;
			top:${str(50 + (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(130 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}


		.slip2_bank_acc {
			font-family:Helvetica;
			font-size:8pt;
			border-width:0px;
			padding-left:0mm;
			padding-top:0mm;
			position:absolute;
			top:${str(42 + (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(90 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}



		.slip2_bank_add_acc {
			font-family:Helvetica;
			font-size:8pt;
			border-width:0px;
			padding-left:0mm;
			padding-top:0mm;
			position:absolute;
			top:${str(160 + (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(65 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}


		.slip2_ref {
			text-align:right;
			font-size:11pt;
			font-family:Helvetica;
			position:absolute;
			top:${str(33 + (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(123 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
			width:78mm;
		}

		.slip2_comp {
			font-family:Helvetica;
			font-size:8pt;
			border-width:0px;
			padding-left:0mm;
			padding-top:0mm;
			position:absolute;
			top:${str(10+ (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(65 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}

		.bvr_background {
			width:210mm;
			height:106mm;
			border:0;
			margin:0;
			position:absolute;
			z-index:-10;
			top:${str(151.2+ (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(0 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}

		.slip2_amount {
			width:5cm;
			text-align:right;
			font-size:11pt;
			font-family:Helvetica;
			position:absolute;
			top:${str(50 + (company.bvr_delta_vert or 0.0)).replace(',','.')}mm;
			left:${str(67 + (company.bvr_delta_horz or 0.0)).replace(',','.')}mm;
		}
		
		.gift_comment {
			font-size: 8px;
			font-weight: bold;
		}

		${css}
		</style>
	</head>
	<body topmargin="0px">
		<% i = 0 %>
		%for partner in objects:
		<% setLang(partner.lang) %>
			%for ref, amount, comment in get_bvrs_data(partner):
				<div style="top: ${i*106}mm; position: relative">
					<!-- slip 1 elements -->
					<div id="slip_address_b" class="slip_address_b">
						<table class="slip_add">
							<tr><td>${ref}</td></tr>
							<tr><td>
								${partner.name |entity}
							</td></tr>
							<tr><td>${partner.street or ''|entity}</td></tr>
							<tr><td>${partner.street2 or ''|entity}</td></tr>
							<tr><td>${partner.zip or ''|entity} ${partner.city or ''|entity}</td></tr>
						</table>
					</div>
					<div id="slip_bank_acc" class="slip_bank_acc">
						${account.get_account_number()}
					</div>
					%if amount:
					<div id="slip_amount" class="slip_amount">
						<span>
							${"&nbsp;".join(_space(('%.2f' % amount)[:-3], 1))}
						</span>  <span style="padding-left:6mm">
							${"&nbsp;".join(_space(('%.2f' % amount)[-2:], 1))}
						</span>
					</div>
					%endif
					<div id="slip_comp" class="slip_comp">
						<table class="slip_add">
							<tr><td>${account.owner_name}</td></tr>
							<tr><td>${account.street}</td></tr>
							<tr><td>${account.zip} ${account.city}</td></tr>
							<tr><td></td></tr>
							<tr><td class="gift_comment">${comment}</td></tr>
						</table>
					</div>

					<!-- slip 2 elements -->
					<div id="slip2_ref" class="slip2_ref" >
						${_space(ref)}
					</div>
					<div id="slip2_address_b" class="slip2_address_b">
						<table class="slip_add">
							<tr><td>
								${partner.name |entity}
							</td></tr>
							<tr><td>${partner.street or ''|entity}</td></tr>
							<tr><td>${partner.street2 or ''|entity}</td></tr>
							<tr><td>${partner.zip or ''|entity} ${partner.city or ''|entity}</td></tr>
						</table>
					</div>
					<div id="slip2_bank_acc" class="slip2_bank_acc">
						${account.get_account_number()}
					</div>
					%if amount:
					<div id="slip2_amount" class="slip2_amount">
						<span>
							${"&nbsp;".join(_space(('%.2f' % amount)[:-3], 1))}
						</span>  <span style="padding-left:6mm">
							${"&nbsp;".join(_space(('%.2f' % amount)[-2:], 1))}
						</span>
					</div>
					%endif
					<div id="slip2_comp" class="slip2_comp">
						<table class="slip_add">
							<tr><td>${account.owner_name}</td></tr>
							<tr><td>${account.street}</td></tr>
							<tr><td>${account.zip} ${account.city}</td></tr>
						</table>
					</div>
				</div>
				<% i += 1 %>
			%endfor
		%endfor
	</body>
</html>
